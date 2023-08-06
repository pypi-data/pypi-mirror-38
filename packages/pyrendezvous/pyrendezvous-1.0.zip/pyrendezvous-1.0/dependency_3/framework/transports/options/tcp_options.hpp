#pragma once

#include <framework/transports/options/options.hpp>


namespace framework {
   
/**
 * @brief Provides TCP socket configuration essentials.
 * 
 * @details
 * This type of configuration can be supplied to all udp based transports. In the 
 * way behavior of the underlying socket can be modified by this configuration.  
 */ 
struct tcp_options : options
{   
    /**
     * @brief The maximum length of the pending connections queue.
     * 
     * @details
     * @para
     * The backlog argument defines the maximum length to which the queue of
     * pending connections for sockfd may grow.  If a connection request
     * arrives when the queue is full, the client may receive an error with
     * an indication of ECONNREFUSED or, if the underlying protocol supports
     * retransmission, the request may be ignored so that a later reattempt
     * at connection succeeds.
     * 
     * @para
     * The behavior of the backlog argument on TCP sockets changed with Linux 2.2. 
     * Now it specifies the queue length for completely established sockets waiting 
     * to be accepted, instead of the number of incomplete connection requests. 
     * The maximum length of the queue for incomplete sockets can be set using 
     * /proc/sys/net/ipv4/tcp_max_syn_backlog. When syncookies are enabled there 
     * is no logical maximum length and this setting is ignored. See tcp(7) 
     * for more information.
     *
     * @para
     * If the backlog argument is greater than the value in /proc/sys/net/core/somaxconn, 
     * then it is silently truncated to that value; the default value in this file is 128. 
     * In kernels before 2.4.25, this limit was a hard coded value, SOMAXCONN, 
     * with the value 128.
     */
    size_t listen_backlog {1};
    
    /**
     * @brief Disables Nagle's algorithm
     * 
     * @details
     * 
     * This means that segments are always sent as soon as possible, even if 
     * there is only a small amount of data. When not set, data is buffered until 
     * there is a sufficient amount to send out, thereby avoiding the frequent 
     * sending of small packets, which results in poor utilization of the network.
     */
    bool no_delay {true};
    
    /**
     * @breif Enable quickack mode.
     * 
     * @details
     * In quickack mode, acks are sent immediately, rather than delayed if needed 
     * in accordance to normal TCP operation. This flag is not permanent, it only 
     * enables a switch to or from quickack mode. Subsequent operation of the TCP 
     * protocol will once again enter/leave quickack mode depending on internal 
     * protocol processing and factors such as delayed ack timeouts occurring and 
     * data transfer. This option should not be used in code intended to be portable.
     */
    bool quick_ack {true};
};

}