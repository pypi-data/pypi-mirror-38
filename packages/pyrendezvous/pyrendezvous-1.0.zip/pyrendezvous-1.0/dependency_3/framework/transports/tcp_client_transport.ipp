#pragma once

#include <cerrno>
#include <chrono>
#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>


namespace framework {

template <typename ip_traits, typename send_buffer, typename allocator>
inline tcp_client_transport<ip_traits, send_buffer, allocator>::tcp_client_transport(
        dispatcher& dispatcher,
        tcp_options options,
        endpoint_type endpoint,
        connected_callback_type connected_callback,
        disconnected_callback_type disconnected_callback,
        receive_callback_type receive_callback,
        error_callback_type error_callback)
    :
        transport(error_callback),
        dispatcher_(dispatcher),
        options_(options),
        endpoint_(endpoint),
        connected_callback_(connected_callback),
        disconnected_callback_(disconnected_callback),
        receive_callback_(receive_callback),
        error_callback_(error_callback),
        allocator_(),
        recv_buffer_guard_(allocator_, options.read_buffer_size),
        recv_buffer_(recv_buffer_guard_),
        send_buffer_(options_.send_buffer_size)
{
    auto socketfd = ::socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, IPPROTO_TCP);
    check_lethal_error(socketfd);

    auto socket_result =::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_RCVBUF,
            &options_.sp_rcvbuf,
            sizeof(options_.sp_rcvbuf));
    check_lethal_error(socket_result);

    socket_result =::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_SNDBUF,
            &options_.sp_sndbuf,
            sizeof(options_.sp_rcvbuf));
    check_lethal_error(socket_result);

    int opt = options_.no_delay;
    socket_result =::setsockopt(
            socketfd,
            IPPROTO_TCP,
            TCP_NODELAY,
            &opt,
            sizeof(opt));
    check_lethal_error(socket_result);

    opt = options_.quick_ack;
    socket_result =::setsockopt(
            socketfd,
            IPPROTO_TCP,
            TCP_QUICKACK,
            &opt,
            sizeof(opt));
    check_lethal_error(socket_result);

    linger lin;
    lin.l_onoff = 1;
    lin.l_linger = 1;
    socket_result =::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_LINGER,
            reinterpret_cast<void*>(&lin),
            sizeof(lin));
    check_lethal_error(socket_result);

    auto fcntl_result = ::fcntl(
            socketfd,
            F_SETFL,
            ::fcntl(socketfd, F_GETFL, NULL) | O_NONBLOCK);
    check_lethal_error(fcntl_result);

    sockaddr_in connect_addr(endpoint_);
    socket_result = ::connect(
            socketfd,
            reinterpret_cast<sockaddr* >(&connect_addr),
            sizeof(connect_addr));
    check_lethal_error(socket_result);

    dispatchable::set_fd(socketfd);

    dispatcher_.add(*this, true, true, true, true);
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline tcp_client_transport<ip_traits, send_buffer, allocator>::~tcp_client_transport()
{
    dispatcher_.remove(*this);
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline bool tcp_client_transport<ip_traits, send_buffer, allocator>::is_connected() const
{
    return is_connected_ && !is_disconnected_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline bool tcp_client_transport<ip_traits, send_buffer, allocator>::has_pending() const
{
    auto& buffer = const_cast<send_buffer&>(send_buffer_);
    return !buffer.empty();
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename data_type>
inline bool tcp_client_transport<ip_traits, send_buffer, allocator>::send(
        const data_type& data)
{
    if (!is_connected_)
        raise_error(EPIPE);

    boost::memory::buffer_ref data_ref(data);

    // try to send first if send buffer is empty
    if (send_buffer_.empty())
    {
        while (true)
        {
            auto send_result = ::send(
                    fd(),
                    data_ref.as_pointer<void*>(),
                    data_ref.length(),
                    0); // MSG_DONTWAIT not required as NONBLOCK set with fnctl

            // when maximum packet size is reached send it in the next batch
            if (send_result > 0 && size_t(send_result) < data_ref.length())
            {
                data_ref = boost::memory::buffer_ref(
                        data_ref.as_pointer<char*>() + send_result,
                        data_ref.length() - send_result);

                continue;
            }

            if (check_error(send_result))
                return true;
            else
                break;
        }
    }

    // enqueue for dispatch if cannot send now
    {
        return send_buffer_.push([&data_ref](auto slot)
        {
            std::memcpy(slot, data_ref.as_pointer<void*>(), data_ref.length());
        }, data_ref.length());
    }
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_client_transport<ip_traits, send_buffer, allocator>::disconnect()
{
    is_disconnected_ = true;
    if (fd() != dispatchable::no_fd)
    {
        ::close(fd());
    }
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_client_transport<ip_traits, send_buffer, allocator>::close()
{
    disconnect();
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename rep, typename period>
inline bool tcp_client_transport<ip_traits, send_buffer, allocator>::wait(std::chrono::duration<rep, period> timeout)
{
    if (send_buffer_.empty())
        return true;

    std::unique_lock<std::mutex> lock(all_sent_mutex_);
    return all_sent_.wait_for(lock, timeout) != std::cv_status::timeout;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_client_transport<ip_traits, send_buffer, allocator>::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    if (!is_connected_)
    {
        int result;
        socklen_t result_len = sizeof(result);
        auto socket_result = ::getsockopt(
                fd(),
                SOL_SOCKET,
                SO_ERROR,
                &result,
                &result_len);
        check_error(socket_result);
        if (result == 0)
        {
            if (connected_callback_)
                connected_callback_(*this);

            is_connected_ = true;
        }
        else
        {
            raise_error(result);
        }
    }

    if (should_receive)
    {
        while (true)
        {
            auto socket_result = ::recv(
                    fd(),
                    recv_buffer_.as_pointer<void*>(),
                    recv_buffer_.length(),
                    0); // non blocking
            if (check_error(socket_result))
            {
                if (socket_result > 0)
                {
                    auto recv_subbuffer_ = recv_buffer_.subbuf(socket_result);
                    if (receive_callback_)
                        receive_callback_(*this, recv_subbuffer_);
                }
                else if (socket_result == 0)
                {
                    if (is_connected_)
                    {
                        is_connected_ = false;
                        if (disconnected_callback_)
                            disconnected_callback_(*this);
                    }

                    break;
                }
            }
            else
            {
                // break when no more data to receive
                break;
            }
        }
    }

    if (should_send)
    {
        auto consume_result = send_buffer_.consume(
                [this](const uint8_t* consumed, size_t size) -> bool
                {
                    while (true)
                    {
                        auto send_result = ::send(
                                fd(),
                                consumed,
                                size,
                                0); // socket is non blocking no need for MSG_DONTWAIT

                        // when maximum packet size is reached send it in the next batch
                        if (send_result > 0 && size_t(send_result) < size)
                        {
                            consumed += send_result;
                            size -= send_result;

                            continue;
                        }

                        return check_error(send_result);
                    }
                });

        if (!consume_result)
            all_sent_.notify_all();
    }

    if (should_disconnect)
    {
        if (is_connected_)
        {
            is_connected_ = false;
            if (disconnected_callback_)
                disconnected_callback_(*this);
        }

        auto close_result = ::close(fd());
        check_error(close_result);

        set_fd(dispatchable::no_fd);
    }
}

template <typename ip_traits, typename send_buffer, typename allocator>
std::ostream& operator<<(std::ostream& os, const tcp_client_transport<ip_traits, send_buffer, allocator>& tr)
{
    os << "tcp:" << tr.endpoint_;
    os << (tr.is_connected() ? "(connected)" : "(disconnected)");
    return os;
}

}

