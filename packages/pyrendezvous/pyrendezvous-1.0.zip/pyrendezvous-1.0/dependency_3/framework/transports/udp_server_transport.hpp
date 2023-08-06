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
 * @brief Provides transport for serving incoming UDP
 *
 * @tparam ip_traits
 * @tparam send_buffer
 * @tparam allocator
 */
template <typename ip_traits, typename send_buffer, typename allocator = boost::memory::mallocator>
class udp_server_transport final : public transport
{
public:
    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    using transport_type = udp_server_transport<ip_traits, send_buffer>;
    using packet_info_type = packet_info<ip_traits>;
    using receive_buffer_type = boost::memory::buffer_ref;
    using receive_callback_type = std::function<void(transport_type&, receive_buffer_type&)>;
    using send_buffer_type = send_buffer;
    using bool_field_type = boost::concurrency::field<size_t>;

    /**
     * @brief
     * @param dispatcher
     * @param options
     * @param endpoint
     * @param receive_callback
     * @param error_callback
     */
    explicit udp_server_transport(
            dispatcher& dispatcher,
            udp_options options,
            endpoint_type endpoint,
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Non-copy constructable.
     */
    udp_server_transport(const udp_server_transport&) = delete;

    /**
     * @brief Destroys **udp_server_transport**.
     */
    ~udp_server_transport();

    /**
     * @brief Endpoint the transport is listening at.
     * @details
     * This method returns either the **endpoint** given during object construction
     * or if the port was set to 0 (random_port) port assigned from the system.
     *
     * @return An endpoint - address and port the transport is listening at.
     */
    endpoint_type at() const;
    /**
     * @brief Indicates if there are any datagrams in the ring buffer awaiting sent.
     * @returns True if there are datagrams awaiting sent, False otherwise.
     */
    bool has_pending() const;
    /**
     * @brief Last packet reception info.
     * @return A const reference to **packet_info** related to the last received packet.
     */
    const packet_info_type& info() const;

    /**
     * @brief Replies to the last received packet.
     * @param data Data object to reply with
     * @tparam data_type Type of the reply data type.
     * @return True if reply sent immediately or queued in internal send buffer, false otherwise.
     */
    template <typename data_type>
    bool reply(const data_type& data);
    /**
     * @brief Closes the underlying socket.
     */
    void close();

    /**
     * @brief Waits until all replies stored in ring buffer are sent.
     * @param timeout Timeout after which the method returns no matter if the send
     * finished or not.
     * @return **true** if there are no more replies to send, **false** on timeout.
     */
    template <typename rep, typename period>
    bool wait(std::chrono::duration<rep, period> timeout);

    /**
     * @brief Non-copy assignable.
     */
    udp_server_transport& operator=(const udp_server_transport&) = delete;

private:
    using allocation_guard_type = boost::memory::allocation_guard<allocator>;

    static constexpr size_t control_buffer_size = 1024;

    template <typename ip_traits_e, typename send_buffer_e, typename allocator_e>
    friend std::ostream& operator<<(
            std::ostream& os,
            const udp_server_transport<ip_traits_e, send_buffer_e, allocator_e>& tr);

    struct reply_data
    {
        static size_t storage_size(size_t datagram_size);
        static size_t data_size(size_t total_length);

        sockaddr_in destination;
        uint8_t data[0];
    };

    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher& dispatcher_;
    udp_options options_;
    endpoint_type endpoint_;

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
 * An example how to write a udp server with **tcp_client_transport**:
 *
 * @example framework/transports/udp_server_transport.cpp
 */

#include "udp_server_transport.ipp"

