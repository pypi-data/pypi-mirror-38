#pragma once

#include <framework/utils/string_utils.hpp>

#include <iostream>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


namespace framework { namespace ip { namespace v4 {

/**
 * @brief IPv4 address.
 * 
 * @details
 * The type is a wrapper around **in_addr** type from BSD socket library. As such 
 * it allows conversion from and to this type as well as other operations.
 */
class address
{
public:
    /**
     * @brief Gets an IPv4 any address representation.
     * 
     * @details
     * Returns address 0.0.0.0 (INADDR_ANY).
     * @return **address** for INADDR_ANY.
     */
    static address any() 
    { 
        return address(htonl(INADDR_ANY));
    }
    
    /**
     * @brief Copy constructor.
     * @param other A source address to copy.
     */
    address(const address& other) = default;
    /**
     * @brief Creates an address from a dot separated string.
     * @param address_str A dot separated string representation of the IPv4 address.
     */
    address(std::string address_str);
    /**
     * @brief Creates an address from a dot separated string.
     * @param address_str A dot separated string representation of the IPv4 address.
     */
    address(const char* address_str);
    /**
     * @brief Creates an **address** from **in_addr**.
     * @param in_addr A reference to **in_addr**.
     */
    address(const in_addr& in_addr);
    
    /**
     * @brief Equality check.
     * @param other Other address to compare.
     * @return **true** if both addresses are equal, **false** otherwise.
     */
    bool operator==(const address& other) const;
    /**
     * @brief Non-equality check.
     * @param other Other address to compare.
     * @return **true** if addresses aren't the same, **false** if they are.
     */
    bool operator!=(const address& other) const;
    /**
     * @brief Implicitly converts into **in_addr**.
     * @return A converted instance of **in_addr**.
     */
    operator in_addr() const;
private:
    friend std::ostream& operator<<(std::ostream& os, const address& addr);
    
    constexpr address(uint32_t other);
    
    in_addr address_;
};

static const address any = address("0.0.0.0");

std::ostream& operator<<(std::ostream& os, const address& addr);

/**
 * @brief Represents an IPv4 endpoint (address + port) for a transport layer protocol.
 */
class endpoint
{
public:
    static constexpr char port_separator = ':';
    static constexpr uint16_t random_port = 0;
    
    /**
     * Non-default constructable.
     */
    endpoint() = delete;
    /**
     * Non-copy constructable.
     */
    endpoint(const endpoint& other) = default;
    /**
     * @brief Constructs an **endpoint** from an **address** and **port**.
     * @param address An IPv4 address
     * @param port A port
     */
    endpoint(const address& address, uint16_t port);
    /**
     * @brief Constructs an endpoint from endpoint string representation.
     * 
     * @details
     * An endpoint string representation has a following form <address string>:<port>.
     * @param endpoint_str An endpoint string.
     */
    endpoint(std::string endpoint_str);
    /**
     * @brief Constructs an endpoint from endpoint string representation.
     * 
     * @details
     * An endpoint string representation has a following form <address string>:<port>.
     * @param endpoint_str An endpoint string.
     */
    endpoint(const char* endpoint_str);
    /**
     * @brief Constructs an **endpoint** from **sockaddr_in**.
     * @param s
     */
    endpoint(const sockaddr_in& s);
    
    /**
     * @brief Gets the address.
     * @return A reference to stored **address**.
     */
    const address& get_address() const;
    /**
     * @brief Gets the port.
     * @return A port number of this endpoint.
     */
    uint16_t get_port() const;
    
    /**
     * @breif Implicitly extracts address definition as **in_addr**
     * @return An instance of **in_addr** holding endpoints address.
     */
    operator in_addr() const;
    operator sockaddr_in() const;
    
    /**
     * @brief Assign address within the endpoint from **in_addr**.
     * @param addr An address to assign to the endpoint.
     * @return A reference to this endpoint.
     */
    endpoint& operator=(const in_addr& addr);
    
    /**
     * @brief Checks equality between two endpoints.
     * 
     * @details
     * Two IPv4 endpoints are equal if their addresses and ports are equal.
     * @param other Other **endpoint** to compare with.
     * @return **true** if equal, **false** otherwise. 
     */
    bool operator==(const endpoint& other) const;
    /**
     * @brief Checks inequality between two endpoints.
     * 
     * @details
     * Two IPv4 endpoints are equal if their addresses and ports are equal.
     * @param other Other **endpoint** to compare with.
     * @return **false** if equal, **true** otherwise. 
     */
    bool operator!=(const endpoint& other) const;
private:
    friend std::ostream& operator<<(std::ostream& os, const endpoint& endp);
    
    static address extract_address(std::string& s);
    static uint16_t extract_port(std::string& s);
    
    address address_;
    uint16_t port_;
};

std::ostream& operator<<(std::ostream& os, const endpoint& endp);

/**
 * @brief Provides reference to address and endpoint traits of IPv4.
 * 
 * @see
 * See [IPv4](https://en.wikipedia.org/wiki/IPv4) information page for more details.
 */
class traits
{
public:
    using address_type = address;
    using endpoint_type = endpoint;
};
    
} } }

#include "ipv4.ipp"

