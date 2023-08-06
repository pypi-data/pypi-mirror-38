#pragma once

#include <framework/dispatcher.hpp>
#include <framework/transports/options/udp_options.hpp>
#include <framework/transports/transport.hpp>

#include <boost/memory.hpp>

#include <chrono>
#include <condition_variable>
#include <mutex>


namespace framework {

/**
 * @brief Sends UDP datagrams to a single IP multicast group
 *
 * @details
 * @para
 * This transport is used as a non-blocking publisher of IP/UDP multicast stream.
 * A single transport binds to a unique stream identified by a group and port. It cannot
 * publish data to any other group.
 *
 * @para
 * Usage example:
 * @code
 * #include <framework/dispatcher.hpp>
 * #include <framework/loop.hpp>
 * #include <framework/transports.hpp>
 *
 * ...
 *
 * framework::dispatcher dispatcher;
 * framework::loop main_loop(dispatcher);
 *
 * framework::udp_options options;
 * framework::ipv4_udp::single_sender::publisher_transport transport(
 *       dispatcher,
 *       options,
 *       "224.0.0.1:27000",
 *       "0.0.0.0",
 *       [](auto& error)
 *       {
 *           cerr << error.what() << endl;
 *       });
 *
 * framework::auto_reload_timer timer(
 *      dispatcher,
 *      30s,
 *      [&transport](framework::auto_reload_timer& source, uint64_t expirations)
 *      {
 *          transport.send("trigger with " + to_string(expirations) + " expirations!");
 *      },
 *      [](exception& error)
 *      {
 *          cerr << error.what() << endl;
 *      });
 * timer.arm();
 *
 * ...
 * @endcode
 *
 * @see
 * More information on IP multicast - http://www.tldp.org/HOWTO/Multicast-HOWTO-2.html
 */
template <typename ip_traits, typename send_buffer>
class udp_publisher_transport final : public transport
{
public:
    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    using transport_type = udp_publisher_transport<ip_traits, send_buffer>;

    /**
     * @brief Initializes an instance of **udp_publisher_transport**.
     * @param dispatcher A dispatcher to attach this publisher with.
     * @param options Options to tune up UDP socket.
     * @param group A multicast group to publish the data to.
     * @param interface An interface on which the data should be published.
     * @param error_callback A callback invoked whenever a non-lethal error occurs.
     */
    explicit udp_publisher_transport(
            dispatcher& dispatcher,
            udp_options options,
            endpoint_type group,
            address_type interface,
            error_callback_type error_callback = {});
    /**
     * @brief Non-copy constructable.
     */
    udp_publisher_transport(const udp_publisher_transport& other) = delete;

    /**
     * @brief Tears down the transport.
     */
    virtual ~udp_publisher_transport();

    /**
     * @brief Indicates if there are any datagrams in the ring buffer awaiting sent.
     * @returns True if there are datagrams awaiting sent, False otherwise.
     */
    bool has_pending() const;

    /**
     * @brief Publishes or enqueues for publication an UDP datagram.
     *
     * @param data The data to send.
     * @tparam data_type A type of data object to send.
     */
    template <typename data_type>
    bool send(const data_type& data);
    /**
     * @brief Closes the underlying socket.
     */
    void close();

    /**
     * @brief Blocks until all data stored in send buffer is sent or timeout is reached.
     * @details
     * Wait method should never be called from dispatch thread as this will cause a deadlock.
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
    udp_publisher_transport& operator=(const udp_publisher_transport&) = delete;

private:
    template <typename ip_traits_e, typename send_buffer_e>
    friend std::ostream& operator<< (
            std::ostream &os,
            const udp_publisher_transport<ip_traits_e, send_buffer_e>& tr);

    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher& dispatcher_;
    udp_options options_;
    endpoint_type group_;
    address_type interface_;

    sockaddr_in destination_;
    send_buffer send_buffer_;

    std::mutex all_sent_mutex_;
    std::condition_variable all_sent_;
};

}

#include "udp_publisher_transport.ipp"

