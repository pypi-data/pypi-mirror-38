#pragma once

#include <arpa/inet.h>
#include <cstdlib>
#include <cstring>
#include <netdb.h>
#include <sstream>
#include <string>
#include <stdexcept>
#include <sys/socket.h>
#include <vector>


namespace framework { namespace ip { namespace v4 {
   
inline address::address(const std::string address_str)
    : address(address_str.c_str())
{
    
}

inline address::address(const char* address_str)
{
    if (::inet_aton(address_str, &address_) == 0)
    {
        auto he = ::gethostbyname(address_str);
        if (he == NULL)
        {
            throw std::logic_error(strerror(errno));
        }
        
        auto addr_list = reinterpret_cast<in_addr**>(he->h_addr_list);
        address_ = *addr_list[0];
    }
}

inline address::address(const in_addr& addr)
    : address_(addr)
{

}

inline constexpr address::address(uint32_t other)
    : address_({ other })
{

}

inline bool address::operator==(const address& other) const
{
    return address_.s_addr == other.address_.s_addr; 
}

inline bool address::operator!=(const address& other) const
{
    return address_.s_addr != other.address_.s_addr; 
}

inline address::operator in_addr() const
{
    return address_;
}

inline std::ostream& operator<<(std::ostream& os, const address& addr)
{
    os << ::inet_ntoa(addr.address_);
    return os;
}

inline endpoint::endpoint(const address& address, uint16_t port)
    : 
        address_(address), 
        port_(port)
{
    
}

inline endpoint::endpoint(std::string endpoint_str)
    : 
        address_(extract_address(endpoint_str)), 
        port_(extract_port(endpoint_str))
{
    
}

inline endpoint::endpoint(const char* endpoint_str)
    : endpoint(std::string(endpoint_str))
{
    
}

inline endpoint::endpoint(const sockaddr_in& s)
    : endpoint(s.sin_addr, ntohs(s.sin_port))
{
    
}

inline const address& endpoint::get_address() const
{
    return address_;
}

inline uint16_t endpoint::get_port() const
{
    return port_;
}

inline endpoint::operator in_addr() const
{
    return address_;
}

inline endpoint::operator sockaddr_in() const
{
    sockaddr_in sa;
    ::bzero(&sa, sizeof(sockaddr_in));
    sa.sin_addr = address_;
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port_);
    
    return sa;
}

inline endpoint& endpoint::operator=(const in_addr& addr)
{
    address_ = addr;
    return *this;
}

inline bool endpoint::operator==(const endpoint& other) const
{
    return address_ == other.address_ && port_ == other.port_;
}

inline bool endpoint::operator!=(const endpoint& other) const
{
    return address_ != other.address_ || port_ != other.port_;
}

inline address endpoint::extract_address(std::string& s)
{
    auto particles = string_utils::split(s, port_separator);
    if (particles.size() != 2)
    {
        std::stringstream ss;
        ss << s << " doesnot describe IPv4 endpoint!";
        
        throw std::invalid_argument(ss.str());
    }
    
    return address(particles.at(0));
}

inline uint16_t endpoint::extract_port(std::string& s)
{
    auto particles = string_utils::split(s, port_separator);
    if (particles.size() != 2)
    {
        std::stringstream ss;
        ss << s << " doesnot describe IPv4 endpoint!";
        
        throw std::invalid_argument(ss.str());
    }
    
    return std::stoi(particles.at(1));
}

inline std::ostream& operator<<(std::ostream& os, const endpoint& endp)
{
    os << endp.get_address() << endpoint::port_separator << endp.get_port();
    return os;
}
    
} } }

