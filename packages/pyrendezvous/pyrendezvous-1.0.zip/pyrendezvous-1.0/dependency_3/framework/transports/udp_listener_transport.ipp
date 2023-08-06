#pragma once

#include <fcntl.h>
#include <netinet/in.h>
#include <sys/socket.h>


namespace framework {

template <typename ip_traits, typename allocator>
inline udp_listener_transport<ip_traits, allocator>::udp_listener_transport(
        dispatcher& dispatcher,
        udp_options options,
        std::vector<address_type>&& groups,
        uint16_t port,
        address_type interface,
        receive_callback_type receive_callback,
        error_callback_type error_callback)
    :
        transport(error_callback),
        dispatcher_(dispatcher),
        options_(options),
        groups_(groups),
        port_(port),
        interface_(interface),
        receive_callback_(receive_callback),
        allocator_(),
        control_buffer_guard_(allocator_, control_buffer_size),
        recv_buffer_guard_(allocator_, options_.read_buffer_size),
        control_buffer_(control_buffer_guard_),
        recv_buffer_(recv_buffer_guard_),
        info_()
{
    auto socketfd = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    check_lethal_error(socketfd);

    int yes = 1;
    auto socket_result = ::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_REUSEADDR,
            &yes,
            sizeof(int));
    check_lethal_error(socket_result);

    socket_result = ::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_REUSEPORT,
            &yes,
            sizeof(int));
    check_lethal_error(socket_result);

    socket_result =::setsockopt(
            socketfd,
            SOL_SOCKET,
            SO_RCVBUF,
            &options_.sp_rcvbuf,
            sizeof(options_.sp_rcvbuf));
    check_lethal_error(socket_result);

    int no = 0;
    socket_result = ::setsockopt(
            socketfd,
            IPPROTO_IP,
            IP_MULTICAST_ALL,
            &no,
            sizeof(int));
    check_lethal_error(socket_result);

    int sp_timestampns = options_.timestampns;
    socket_result =::setsockopt(
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

    endpoint_type port_endpoint(address_type::any(), port_);
    sockaddr_in group_address(port_endpoint);
    socket_result = ::bind(
            socketfd,
            reinterpret_cast<sockaddr* >(&group_address),
            sizeof(group_address));
    check_lethal_error(socket_result);

    for (auto& group : groups_)
    {
        if (interface_ != address_type::any())
        {
            ip_mreq mref;
            mref.imr_interface = interface_;
            mref.imr_multiaddr = group;
            socket_result = ::setsockopt(
                    socketfd,
                    IPPROTO_IP,
                    IP_ADD_MEMBERSHIP,
                    &mref,
                    sizeof(ip_mreq));
            check_lethal_error(socket_result);
        }
        else
        {
            ip_mreq mref;
            mref.imr_interface = address_type::any();
            mref.imr_multiaddr = group;
            socket_result = ::setsockopt(
                    socketfd,
                    IPPROTO_IP,
                    IP_ADD_MEMBERSHIP,
                    &mref,
                    sizeof(ip_mreq));
            check_lethal_error(socket_result);
        }
    }

    dispatchable::set_fd(socketfd);
    dispatcher_.add(*this, true, false, false, true);
}

template <typename ip_traits, typename allocator>
inline udp_listener_transport<ip_traits, allocator>::udp_listener_transport(
        dispatcher& dispatcher,
        udp_options options,
        endpoint_type group,
        address_type interface,
        receive_callback_type receive_callback,
        error_callback_type error_callback)
    :
        udp_listener_transport(
                dispatcher,
                options,
                { group.get_address() },
                group.get_port(),
                interface,
                receive_callback,
                error_callback)
{

}

template <typename ip_traits, typename allocator>
inline udp_listener_transport<ip_traits, allocator>::~udp_listener_transport()
{
    dispatcher_.remove(*this);
}

template <typename ip_traits, typename allocator>
inline const typename udp_listener_transport<ip_traits, allocator>::packet_info_type& udp_listener_transport<ip_traits, allocator>::info() const
{
    return info_;
}

template <typename ip_traits, typename allocator>
inline void udp_listener_transport<ip_traits, allocator>::close()
{
    if (fd() != dispatchable::no_fd)
        ::close(fd());
}


template <typename ip_traits, typename allocator>
inline void udp_listener_transport<ip_traits, allocator>::handle_event(
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
                    else if (cmsg->cmsg_level == IPPROTO_IP)
                    {
                        if (cmsg->cmsg_type == IP_PKTINFO)
                        {
                            auto& pktinfo = *reinterpret_cast<in_pktinfo*>(CMSG_DATA(cmsg));
                            info_data.from = {pktinfo.ipi_addr, port_};
                        }
                    }
                }

                clock_gettime(CLOCK_REALTIME, &info_data.read_time);
                if (receive_callback_)
                    receive_callback_(*this, recv_subbuffer);
            }
            else
            {
                // no more data pending
                break;
            }
        }
    }
}

template <typename ip_traits, typename allocator>
inline std::ostream& operator<< (std::ostream &os, const udp_listener_transport<ip_traits, allocator>& tr)
{
    os << "udp_multicast_listen:";

    auto index = 0;
    for (auto& group : tr.groups_)
    {
        if (index++ > 0)
            os << ",";
        os << group << ":" << tr.port_;
    }
    os << "[" << tr.interface_ << "]";

    return os;
}

}

