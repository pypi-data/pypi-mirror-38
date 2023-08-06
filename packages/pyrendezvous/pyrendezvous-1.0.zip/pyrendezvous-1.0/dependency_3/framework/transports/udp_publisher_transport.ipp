#pragma once

#include <fcntl.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <thread>


namespace framework {

template <typename ip_traits, typename send_buffer>
inline udp_publisher_transport<ip_traits, send_buffer>::udp_publisher_transport(
        dispatcher& dispatcher,
        udp_options options,
        endpoint_type group,
        address_type interface,
        error_callback_type error_callback)
    :
        transport(error_callback),
        dispatcher_(dispatcher),
        options_(options),
        group_(group),
        interface_(interface),
        destination_(group),
        send_buffer_(options.send_buffer_size)
{
    auto socketfd = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    check_lethal_error(socketfd);

    auto socket_result = ::setsockopt(
            socketfd,
            IPPROTO_IP,
            IP_MULTICAST_TTL,
            &options.ttl,
            sizeof(options.ttl));
    check_lethal_error(socket_result);

    int opt = options.loop;
    socket_result = ::setsockopt(
            socketfd,
            IPPROTO_IP,
            IP_MULTICAST_LOOP,
            &opt,
            sizeof(int));
    check_lethal_error(socket_result);

    int yes = 1;
    socket_result = ::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_REUSEADDR,
            &yes,
            sizeof(int));
    check_lethal_error(socket_result);

    socket_result =::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_SNDBUF,
            &options_.sp_sndbuf,
            sizeof(options_.sp_rcvbuf));
    check_lethal_error(socket_result);

    auto fcntl_result = ::fcntl(
            socketfd,
            F_SETFL,
            ::fcntl(socketfd, F_GETFL, NULL) | O_NONBLOCK);
    check_lethal_error(fcntl_result);

    if (interface_ != address_type::any())
    {
        // required for sending
        in_addr interface_addr(interface_);
        socket_result = ::setsockopt(
                socketfd,
                SOL_IP,
                IP_MULTICAST_IF,
                &interface_addr,
                sizeof(interface_addr));
        check_lethal_error(socket_result);
    }

    dispatchable::set_fd(socketfd);
    dispatcher_.add(*this, false, true, false, true);
}

template <typename ip_traits, typename send_buffer>
inline udp_publisher_transport<ip_traits, send_buffer>::~udp_publisher_transport()
{
    dispatcher_.remove(*this);
}

template <typename ip_traits, typename send_buffer>
inline bool udp_publisher_transport<ip_traits, send_buffer>::has_pending() const
{
    auto& buffer = const_cast<send_buffer&>(send_buffer_);
    return !buffer.empty();
}

template <typename ip_traits, typename send_buffer>
template <typename data_type>
inline bool udp_publisher_transport<ip_traits, send_buffer>::send(
        const data_type& data)
{
    boost::memory::buffer_ref data_ref(data);

    // try to send first if ring buffer is empty
    if (send_buffer_.empty())
    {
        while (true)
        {
            auto send_result = ::sendto(
                    fd(),
                    data_ref.as_pointer<void*>(),
                    data_ref.length(),
                    0,
                    reinterpret_cast<sockaddr*>(&destination_),
                    sizeof(sockaddr_in));

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

template <typename ip_traits, typename send_buffer>
void udp_publisher_transport<ip_traits, send_buffer>::handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect)
{
    if (should_send)
    {
        auto send_result = send_buffer_.consume([this](const uint8_t* consumed, size_t size) -> bool
        {
            while (true)
            {
                auto send_result = ::sendto(
                        fd(),
                        consumed,
                        size,
                        0, // MSG_DONTWAIT not required as NONBLOCK set with fnctl
                        reinterpret_cast<sockaddr*>(&destination_),
                        sizeof(sockaddr_in));

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

        if (!send_result)
            all_sent_.notify_all();
    }
}

template <typename ip_traits, typename allocator>
inline void udp_publisher_transport<ip_traits, allocator>::close()
{
    if (fd() != dispatchable::no_fd)
        ::close(fd());
}

template <typename ip_traits, typename send_buffer>
template <typename rep, typename period>
inline bool udp_publisher_transport<ip_traits, send_buffer>::wait(std::chrono::duration<rep, period> timeout)
{
    if (send_buffer_.empty())
        return true;

    std::unique_lock<std::mutex> lock(all_sent_mutex_);
    return all_sent_.wait_for(lock, timeout) != std::cv_status::timeout;
}

template <typename ip_traits, typename send_buffer>
inline std::ostream& operator<< (
        std::ostream &os,
        const udp_publisher_transport<ip_traits, send_buffer>& tr)
{
    os << "udp_mulicast_publish:";
    os << tr.group_ << "[" << tr.interface_ << "]";
    return os;
}

}

