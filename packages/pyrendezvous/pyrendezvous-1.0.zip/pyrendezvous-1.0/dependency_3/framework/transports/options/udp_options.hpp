#pragma once

#include <framework/transports/options/options.hpp>

#include <cstddef>
#include <cstdint>


namespace framework {

/**
 * @brief Provides UDP configuration essentials.
 *
 * @details
 * This type of configuration can be supplied to all udp based transports. In the
 * way behavior of the underlying socket can be modified by this configuration.
 */
struct udp_options : options
{
    /**
     * @brief Decides if sent data should be looped to the sending host.
     *
     * @details
     * @para
     * Unless this property is set to **true** system will not route sent multicast
     * packets to any socket listening to the stream at the host the packet is originating 
     * from.
     * 
     * @para
     * This options is only valid for publication to an IP/UDP multicast group.
     * It does not relate to unicast communication. Setting this options is an
     * equivalent of setting **IPPROTO_IP/IP_MULTICAST_LOOP** socket option.
     * 
     * @see
     * [IPPROTO_IP/IP_MULTICAST_LOOP](http://man7.org/linux/man-pages/man7/ip.7.html)
     */
    bool loop {true};

    /**
     * @brief Defines TTL on sent IP/UDP multicast packets.
     *
     * @details
     * @para
     * Set or retrieve the current time-to-live field that is used in every packet 
     * sent from the transport. Default 1.
     * 
     * @para
     * This property is propagated into BSD socket option **IPPROTO_IP/IP_MULTICAST_TTL**.
     * 
     * @see
     * [IPPROTO_IP/IP_MULTICAST_TTL](http://man7.org/linux/man-pages/man7/ip.7.html)
     */
    uint8_t ttl {1};

    /**
     * @brief Generates a timestamp for each incoming packet.
     *
     * @details
     * This socket option enables timestamping of datagrams on the reception
     * path. Because the destination socket, if any, is not known early in
     * the network stack, the feature has to be enabled for all packets. The
     * same is true for all early receive timestamp options.
     */
    bool timestampns {true};

    /**
     * @brief Enables packet details retrieval on packet reception.
     *
     * @details
     * @para
     * Enables reception of  ancillary message for received packet. This structure
     * contains information such as source IP address and interface index.
     * 
     * @para
     * For transports using BSD compatible sockets it's an equivalent of setting 
     * **IPPROTO_IP/IP_PKTINFO** socket option. 
     * 
     * @see
     * [IP_PKTINFO](https://linux.die.net/man/7/ip)
     */
    bool pktinfo {true};
};

}

