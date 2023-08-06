#pragma once

#include <chrono>
#include <ctime>


namespace framework {
  
/**
 * @brief Info about received packet.
 */    
template <typename ip_traits>
class packet_info
{
public:
    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    
    /**
     * @brief Raw data storage for packet info.
     * 
     * @details
     * A reference to raw data storage can be obtained with **packet_info::data**.
     * It must not be accessed outside of the transport code itself, client code should 
     * not modify the raw data.
     */
    struct raw_data
    {
        endpoint_type from{address_type::any(), 0};
    
        timespec receive_time{};
        timespec read_time{};
    };
    
    /**
     * @brief Endpoint from which the buffer has been received
     * 
     * @details
     * @para
     * For multicast stream it's a destination multicast group and port on which 
     * the data was sent. For tcp connection it's report address and port. 
     * 
     * @para
     * This property is universal for both IPv4 and IPv6 and delegates network 
     * definition of the endpoint to traited types for either of the protocols.
     * 
     * @return Address from which buffer has been received.
     */
    const endpoint_type& from() const;
    
    /**
     * @brief Time of packet reception by the network adapter.
     * 
     * @details
     * The source of this time is dependent on the implementation of transport 
     * through which the buffer has been received. Nevertheless, it should have 
     * nanosecond precision and should be comparable to [**clock_gettime(CLOCK_REALTIME)**]
     * (https://linux.die.net/man/3/clock_gettime).
     * 
     * @return A reference to **timespec** structure which can be read and updated from outside
     * of this class.
     */
    std::chrono::system_clock::time_point receive_time() const;
    
    /**
     * @brief Time when the buffer was read by the transport from internal buffers.
     * 
     * @details
     * The source of this time is triggered when transport reads the buffer from underlying
     * system/driver buffer. This time should be comparable to [**clock_gettime(CLOCK_REALTIME)**]
     * (https://linux.die.net/man/3/clock_gettime). 
     * 
     * @return A reference to **timespec** carrying read time.
     */
    std::chrono::system_clock::time_point read_time() const;
    
    /**
     * @brief Calculates time since reception on socket and in the transport.
     * 
     * @details 
     * @para
     * This method returns a tuple with two [durations](http://en.cppreference.com/w/cpp/chrono/duration):
     * * { interval since **receive_time**, interval since **read_time** }. Both times
     * have nanosecond precision. 
     * 
     * @para
     * **Example**
     * @code
     * 
     * #include <iostream>
     * #include <tuple>
     * 
     * void print_intervals(framework::receive_buffer<framework::ip::v4::traits> buffer)
     * {
     *      std::chrono::nanoseconds since_receive;
     *      std::chrono::nanoseconds since_read;
     *      std::tie(since_receive, since_read) = buffer.since();
     * 
     *      std::cout << since_receive << " " << since_read << std::endl;
     * }
     * 
     * @endcode
     * 
     * @return A tuple holding durations since noted **reception_time** and **read_time**.
     */
    auto since() const;
    
    /**
     * @brief Access to info data store.
     */
    raw_data& data();
    
private:
    raw_data data_;
};
    
}

#include "packet_info.ipp"
