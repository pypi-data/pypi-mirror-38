#pragma once

#include <framework/dispatcher.hpp>
#include <framework/transports/options/udp_options.hpp>
#include <framework/transports/packet_info.hpp>
#include <framework/transports/transport.hpp>

#include <boost/concurrency.hpp>
#include <boost/memory.hpp>

#include <chrono>
#include <cerrno>
#include <condition_variable>
#include <functional>
#include <mutex>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <thread>


namespace framework {

/**
 * @brief Provides access to User Datagram Protocol (UDP) network services.
 *
 * @details
 * @para
 * This class provides simple methods for sending and receiving connectionless UDP
 * datagrams in non-blocking mode.
 *
 * @para
 * Even if UDP doesn't support connections as such, this transport can be used
 * to communicate with only a single remote UDP host on a given port. The transport
 * binds itself to a random local port. This is required to receive proper reply
 * datagrams over UDP. Only datagrams originating from the given remote endpoint
 * will be accepted upon reception.
 *
 * @para
 * This transport acts only as a client to UDP unicast communication.
 * **udp_listener_transport** should be used for subscription to UDP multicast.
 *
 * @tparam ip_traits Traits of IP protocol used (either IPv4 or IPv6 defined in
 * **framework::ip**)
 * @tparam send_buffer A type of send buffer. This should be one of variable ring buffers
 * defined in [**boost::concurrency**](https://lukaszlaszko.bitbucket.io/circular_buffers.git/master/).
 * @tparam allocator An allocator used to allocate transport local buffers (send, reception
 * and control buffers) from [**boost::memory**](https://lukaszlaszko.bitbucket.io/allocators.git/master/).
 * By default **boost::mamory::mallocator** is used.
 */
template <typename ip_traits, typename send_buffer, typename allocator = boost::memory::mallocator>
class udp_client_transport final : public transport
{
public:
    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    using transport_type = udp_client_transport<ip_traits, send_buffer>;
    using packet_info_type = packet_info<ip_traits>;
    using receive_buffer_type = boost::memory::buffer_ref;
    using receive_callback_type = std::function<void(transport_type&, receive_buffer_type&)>;
    using send_buffer_type = send_buffer;
    using bool_field_type = boost::concurrency::field<size_t>;

    /**
     * @brief Initializes an instance of **udp_client_transport**.
     *
     * @param dispatcher A **dispatcher** to register this transport with.
     * @param options A range of **udp_option**s exercised by this transport.
     * @param endpoint An endpoint this transport should send datagrams to
     * and received datagrams from.
     * @param receive_callback A callback invoked whenever new data from the remote
     * endpoint directed to this transport is received.
     * @param error_callback An error callback invoked whenever an error is discovered.
     */
    explicit udp_client_transport(
            dispatcher& dispatcher,
            udp_options options,
            endpoint_type endpoint,
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Non-copy constructable.
     */
    udp_client_transport(const udp_client_transport&) = delete;

    /**
     * @brief Tears down an instance of **udp_client_transport**.
     */
    ~udp_client_transport();

    /**
     * @brief Indicates if there are any datagrams in the ring buffer awaiting sent.
     * @returns True if there are datagrams awaiting sent, False otherwise.
     */
    bool has_pending() const;
    /**
     * @brief Last packet reception info.
     *
     * @return A const reference to **packet_info** related to the last received packet.
     */
    const packet_info_type& info() const;

    /**
     * @brief Sends or schedules send of UDP datagram to remote host.
     *
     * @param data The data to send.
     * @tparam data_type Type of data object to send.
     */
    template <typename data_type>
    bool send(const data_type& data);

    /**
     * @brief Closes the underlying socket.
     */
    void close();

    /**
     * @brief Blocks until all data stored in send buffer is sent or timeout is reached.
      *
     * @param timeout Timeout after which the method returns no matter if the send
     * finished or not.
     * @return **true** if send buffer is empty, **false** on timeout.
     */
    template <typename rep, typename period>
    bool wait(std::chrono::duration<rep, period> timeout);

    /**
     * @brief Non-copy assignable.
     */
    udp_client_transport& operator=(const udp_client_transport&) = delete;

private:
    using allocation_guard_type = boost::memory::allocation_guard<allocator>;

    static constexpr size_t control_buffer_size = 1024;

    template <typename ip_traits_e, typename send_buffer_e, typename allocator_e>
    friend std::ostream& operator<<(
            std::ostream& os,
            const udp_client_transport<ip_traits_e, send_buffer_e, allocator_e>& tr);

    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher& dispatcher_;
    udp_options options_;
    sockaddr_in destination_;

    receive_callback_type receive_callback_;

    allocator allocator_;
    allocation_guard_type control_buffer_guard_;
    allocation_guard_type recv_buffer_guard_;

    receive_buffer_type control_buffer_;
    receive_buffer_type recv_buffer_;
    packet_info_type info_;

    send_buffer_type send_buffer_;

    std::mutex all_sent_mutex_;
    std::condition_variable all_sent_;
};

}

/**
 * An example how to write a udp client with **tcp_client_transport**:
 *
 * @example framework/transports/udp_client_transport.cpp
 */

#include "udp_client_transport.ipp"

