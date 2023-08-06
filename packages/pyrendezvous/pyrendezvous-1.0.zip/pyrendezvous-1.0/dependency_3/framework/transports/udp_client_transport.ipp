#pragma once

#include <fcntl.h>


namespace framework {

template <typename ip_traits, typename send_buffer, typename allocator>
inline udp_client_transport<ip_traits, send_buffer, allocator>::udp_client_transport(
        dispatcher& dispatcher,
        udp_options options,
        endpoint_type endpoint,
        receive_callback_type receive_callback,
        error_callback_type error_callback)
    :
        transport(error_callback),
        dispatcher_(dispatcher),
        options_(options),
        destination_(endpoint),
        receive_callback_(receive_callback),
        allocator_(),
        control_buffer_guard_(allocator_, control_buffer_size),
        recv_buffer_guard_(allocator_, options_.read_buffer_size),
        control_buffer_(control_buffer_guard_),
        recv_buffer_(recv_buffer_guard_),
        info_(),
        send_buffer_(options_.send_buffer_size)
{
    auto socketfd = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    check_lethal_error(socketfd);

    int sp_timestampns = options_.timestampns;
    auto socket_result =::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_TIMESTAMPNS,
            &sp_timestampns,
            sizeof(sp_timestampns));
    check_lethal_error(socket_result);

    int pktinfo = options_.pktinfo;
    socket_result =::setsockopt(
            socketfd,
            IPPROTO_IP,
            IP_PKTINFO,
            &pktinfo,
            sizeof(pktinfo));
    check_lethal_error(socket_result);

    auto fcntl_result = ::fcntl(
            socketfd,
            F_SETFL,
            ::fcntl(socketfd, F_GETFL, NULL) | O_NONBLOCK);
    check_lethal_error(fcntl_result);

    sockaddr_in bind_addr(
            endpoint_type(
                    address_type::any(),
                    endpoint_type::random_port));
    socket_result = ::bind(
            socketfd,
            reinterpret_cast<sockaddr* >(&bind_addr),
            sizeof(bind_addr));
    check_lethal_error(socket_result);

    sockaddr_in sin;
    uint32_t len_inet = sizeof(sockaddr_in);
    socket_result = ::getsockname(
            socketfd,
            reinterpret_cast<sockaddr*>(&sin),
            &len_inet);
    check_lethal_error(socket_result);

    auto& info_data = info_.data();
    info_data.from = endpoint;

    dispatchable::set_fd(socketfd);
    dispatcher_.add(*this, true, true, false, true);
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline udp_client_transport<ip_traits, send_buffer, allocator>::~udp_client_transport()
{
    dispatcher_.remove(*this);
}

template <typename ip_traits, typename send_buffer, typename allocator>
bool udp_client_transport<ip_traits, send_buffer, allocator>::has_pending() const
{
    auto& buffer = const_cast<send_buffer&>(send_buffer_);
    return !buffer.empty();
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline const typename udp_client_transport<ip_traits, send_buffer, allocator>::packet_info_type&
        udp_client_transport<ip_traits, send_buffer, allocator>::info() const
{
    return info_;
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename data_type>
inline bool udp_client_transport<ip_traits, send_buffer, allocator>::send(const data_type& data)
{
    boost::memory::buffer_ref data_ref(data);

    // try to send first if send buffer is empty
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
            if (send_result > 0 && send_result < data_ref.length())
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
inline void udp_client_transport<ip_traits, send_buffer, allocator>::close()
{
    if (fd() != dispatchable::no_fd)
        ::close(fd());
}

template <typename ip_traits, typename send_buffer, typename allocator>
template <typename rep, typename period>
inline bool udp_client_transport<ip_traits, send_buffer, allocator>::wait(std::chrono::duration<rep, period> timeout)
{
    if (send_buffer_.empty())
        return true;

    std::unique_lock<std::mutex> lk(all_sent_mutex_);
    return all_sent_.wait_for(lk, timeout) != std::cv_status::timeout;
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline void udp_client_transport<ip_traits, send_buffer, allocator>::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    if (should_receive)
    {
        while (true)
        {
            msghdr msg;
            iovec iov;

            sockaddr_in host_address;

            iov.iov_base = recv_buffer_.as_pointer<void*>();
            iov.iov_len = recv_buffer_.length();
            msg.msg_iov = &iov;
            msg.msg_iovlen = 1;
            msg.msg_name = &host_address;
            msg.msg_namelen = sizeof(sockaddr_in);
            msg.msg_control = control_buffer_.as_pointer<void*>();
            msg.msg_controllen = control_buffer_.length();

            auto socket_result = ::recvmsg(
                    fd(),
                    &msg,
                    0); // MSG_DONTWAIT not required as NONBLOCK set with fnctl
            if (check_error(socket_result))
            {
                if (std::memcmp(&destination_, &host_address, sizeof(sockaddr_in)) == 0)
                {
                    auto recv_subbuffer = recv_buffer_.subbuf(socket_result);
                    auto& info_data = info_.data();
                    for (auto cmsg = CMSG_FIRSTHDR(&msg);
                         cmsg != NULL;
                         cmsg = CMSG_NXTHDR(&msg, cmsg))
                    {
                        if (cmsg->cmsg_level == SOL_SOCKET)
                        {
                            if (cmsg->cmsg_type == SO_TIMESTAMPNS)
                            {
                                info_data.receive_time = *reinterpret_cast<timespec*>(CMSG_DATA(cmsg));
                            }
                        }
                    }

                    clock_gettime(CLOCK_REALTIME, &info_data.read_time);
                    if (receive_callback_)
                        receive_callback_(*this, recv_subbuffer);
                }
            }
            else
            {
                // Nothing else to receive, break
                break;
            }
        }
    }

    if (should_send)
    {
        auto consume_result = send_buffer_.consume([this](const uint8_t* consumed, size_t size) -> bool
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
    }
}

template <typename ip_traits, typename send_buffer, typename allocator>
inline std::ostream& operator<<(std::ostream& os, const udp_client_transport<ip_traits, send_buffer, allocator>& tr)
{
    os << "udp[client]:" << tr.info_.from();
    return os;
}

}

