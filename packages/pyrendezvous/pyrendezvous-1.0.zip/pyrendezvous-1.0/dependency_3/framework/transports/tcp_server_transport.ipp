#pragma once

#include <cerrno>
#include <iostream>
#include <thread>

#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>

#include "options/tcp_options.hpp"
#include "tcp_server_transport.hpp"


namespace framework {

template <typename ip_traits, typename send_buffer, typename allocator>
inline tcp_server_transport<ip_traits, send_buffer, allocator>::tcp_server_transport(
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
        error_callback_(error_callback)
{
    auto socketfd = ::socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    check_lethal_error(socketfd);

    linger lin;
    lin.l_onoff = 1;
    lin.l_linger = 1;
    auto socket_result =::setsockopt(
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

    sockaddr_in bind_addr(endpoint_);
    socket_result = ::bind(
            socketfd,
            reinterpret_cast<sockaddr* >(&bind_addr),
            sizeof(bind_addr));
    check_lethal_error(socket_result);

    if (endpoint.get_port() == endpoint_type::random_port)
    {
        sockaddr_in sin;
        uint32_t len_inet = sizeof(sockaddr_in);
        socket_result = ::getsockname(
                socketfd,
                reinterpret_cast<sockaddr*>(&sin),
                &len_inet);
        check_lethal_error(socket_result);

        endpoint_ = { endpoint.get_address(), ntohs(sin.sin_port) };
    }

    socket_result = ::listen(
            socketfd,
            options_.listen_backlog);
    check_lethal_error(socket_result);

    dispatchable::set_fd(socketfd);
    dispatcher_.add(*this, true, false, false, true);
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline tcp_server_transport<ip_traits, send_buffer, allocator>::~tcp_server_transport()
{
    connected_clients_.clear();

    dispatcher_.remove(*this);

    auto close_result = ::close(fd());
    check_error(close_result);
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline typename ip_traits::endpoint_type tcp_server_transport<ip_traits, send_buffer, allocator>::at() const
{
    return endpoint_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::close()
{
    if (fd() != dispatchable::no_fd)
        ::close(fd());
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    while (true)
    {
        sockaddr_in client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        auto socket_result = ::accept(
                fd(),
                reinterpret_cast<sockaddr* >(&client_addr),
                &client_addr_len);
        if (check_error(socket_result))
        {
            connected_clients_.emplace_back(
                    dispatcher_,
                    socket_result,
                    allocator_,
                    endpoint_,
                    client_addr,
                    options_,
                    [this](auto& disconnected_transport)
                    {
                        if (disconnected_callback_)
                            disconnected_callback_(disconnected_transport);

                        connected_clients_.remove(disconnected_transport);
                    },
                    receive_callback_,
                    error_callback_);

            if (connected_callback_)
                connected_callback_(connected_clients_.back());
        }
        else
        {
            // no more connecting clients, break the loop
            break;
        }
    }
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::connected_client_transport(
        dispatcher& dispatcher,
        int socketfd,
        allocator& alloc,
        endpoint_type server_endpoint,
        endpoint_type client_endpoint,
        tcp_options options,
        disconnected_callback_type disconnected_callback,
        receive_callback_type receive_callback,
        error_callback_type error_callback)
    :
        transport(error_callback),
        id_(socketfd),
        server_endpoint_(server_endpoint),
        client_endpoint_(client_endpoint),
        dispatcher_(dispatcher),
        options_(options),
        disconnected_callback_(disconnected_callback),
        receive_callback_(receive_callback),
        recv_buffer_guard_(alloc, options.read_buffer_size),
        recv_buffer_(recv_buffer_guard_),
        send_buffer_(options_.send_buffer_size)
{
    dispatchable::set_fd(socketfd);

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

    auto fcntl_result = ::fcntl(
            socketfd,
            F_SETFL,
            ::fcntl(socketfd, F_GETFL, NULL) | O_NONBLOCK);
    check_lethal_error(fcntl_result);

    info_.data().from = client_endpoint_;
    dispatcher_.add(*this, true, true, true, true);
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::~connected_client_transport()
{
    dispatcher_.remove(*this);

    auto close_result = ::close(fd());
    check_error(close_result);
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename data_type>
inline bool tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::send(
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
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::disconnect()
{
    is_disconnected_ = true;
    if (fd() != dispatchable::no_fd)
    {
        ::shutdown(fd(), SHUT_RDWR);
    }
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::close()
{
    disconnect();
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename rep, typename period>
inline bool tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::wait(
        std::chrono::duration<rep, period> timeout)
{
    if (send_buffer_.empty())
        return true;

    std::unique_lock<std::mutex> lock(all_sent_mutex_);
    return all_sent_.wait_for(lock, timeout) != std::cv_status::timeout;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline int tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::id() const
{
    return id_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline typename tcp_server_transport<ip_traits, send_buffer, allocator>::endpoint_type
        tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::from() const
{
    return client_endpoint_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline bool tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::has_pending() const
{
    auto& buffer = const_cast<send_buffer&>(send_buffer_);
    return !buffer.empty();
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline const typename tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::packet_info_type&
        tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::info() const
{
    return info_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline bool tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::is_connected() const
{
    return is_connected_ && !is_disconnected_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename closure_type>
inline boost::optional<closure_type&> tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport
        ::closure()
{
    using noref_type = typename std::remove_reference<closure_type>::type;

    if (closure_.empty())
        return boost::none;

    auto pointer = boost::any_cast<noref_type*>(&closure_);
    if (pointer)
        return *static_cast<closure_type*>(*pointer);

    return boost::any_cast<closure_type&>(closure_);
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename closure_type>
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::set_closure(
        closure_type&& data)
{
    closure_ = std::move(data);
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename closure_type>
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::set_closure(
        closure_type* pointer)
{
    closure_ = pointer;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    if (should_disconnect)
    {
        if (is_connected_)
        {
            is_connected_ = false;
            if (disconnected_callback_)
                disconnected_callback_(*this);
        }

        return;
    }

    if (should_receive)
    {
        while (true)
        {
            auto socket_result = ::recv(
                    fd(),
                    recv_buffer_.as_pointer<void*>(),
                    recv_buffer_.length(),
                    0); // MSG_DONTWAIT not required as NONBLOCK set with fnctl
            if (check_error(socket_result))
            {
                if (socket_result > 0)
                {
                    auto recv_subbuffer = recv_buffer_.subbuf(socket_result);
                    auto& info_data = info_.data();

                    clock_gettime(CLOCK_REALTIME, &info_data.read_time);
                    if (receive_callback_)
                        receive_callback_(*this, recv_subbuffer);
                }
                else
                {
                    if (is_connected_)
                    {
                        is_connected_ = false;
                        if (disconnected_callback_)
                            disconnected_callback_(*this);
                    }

                    // return immediately if disconnected
                    return;
                }
            }
            else
            {
                // no more data to receive, break
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
                                0); // MSG_DONTWAIT not required as NONBLOCK set with fnctl

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
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline bool tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport
        ::operator ==(const connected_client_transport& other) const
{
    return id_ == other.id_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline bool tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport
        ::operator<(const connected_client_transport& other) const
{
    return id_ < other.id_;
}

}