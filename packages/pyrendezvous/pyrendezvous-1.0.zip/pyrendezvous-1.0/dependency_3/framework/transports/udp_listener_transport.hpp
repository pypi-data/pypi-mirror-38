#pragma once

#include <framework/dispatcher.hpp>
#include <framework/transports/options/udp_options.hpp>
#include <framework/transports/packet_info.hpp>
#include <framework/transports/transport.hpp>

#include <boost/memory.hpp>

#include <functional>
#include <iostream>
#include <netinet/in.h>
#include <vector>


namespace framework {

/**
 * @brief A client transport for UDP multicast.
 *
 * @details
 * @para
 * Provides means for subscription to udp multicast on one or multiple multicast groups
 * using a single underlying socket.
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
 * framework::ipv4_udp::listener_transport transport(
 *       dispatcher,
 *       options,
 *       "224.0.0.100:32000",
 *       "0.0.0.0",
 *       [](auto& source, auto& buffer)
 *       {
 *           cerr << "received " << buffer.length() << " bytes from " << source << endl;
 *       },
 *       [](auto& error)
 *       {
 *           cerr << error.what() << endl;
 *       });
 *
 * main_loop.interrupt_on(SIGKILL);
 * main_loop.run_forever();
 *
 * ...
 * @endcode
 *
 * @see
 * More information on IP multicast - http://www.tldp.org/HOWTO/Multicast-HOWTO-2.html
 */
template <typename ip_traits, typename allocator = boost::memory::mallocator>
class udp_listener_transport final : public transport
{
public:
    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    using transport_type = udp_listener_transport<ip_traits>;
    using packet_info_type = packet_info<ip_traits>;
    using receive_buffer_type = boost::memory::buffer_ref;
    using receive_callback_type = std::function<
            void(transport_type&, receive_buffer_type&)>;

    /**
     * @brief Creates an instance of **udp_listener_transport**.
     * @param dispatcher A dispatcher to process invcoming traffic.
     * @param options UDP options.
     * @param groups Multicast groups this listener should listen to.
     * @param port UDP port this listener is for.
     * @param interface Interface on which the listener should listen.
     * @param receive_callback A callback invoked when a new datagram is received.
     * @param error_callback A callback invoked on error.
     */
    explicit udp_listener_transport(
            dispatcher& dispatcher,
            udp_options options,
            std::vector<address_type>&& groups,
            uint16_t port,
            address_type interface,
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Creates an instance of **udp_listener_transport**.
     * @param dispatcher A dispatcher to process invcoming traffic.
     * @param options UDP options.
     * @param group Multicast group and port to listen for.
     * @param interface Interface on which the listener should listen.
     * @param receive_callback A callback invoked when a new datagram is received.
     * @param error_callback A callback invoked on error.
     */
    explicit udp_listener_transport(
            dispatcher& dispatcher,
            udp_options options,
            endpoint_type group,
            address_type interface,
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Non-copy constructable.
     */
    udp_listener_transport(const udp_listener_transport&) = delete;

    /**
     * @brief Destroys this instance of **udp_listener_transport**.
     */
    virtual ~udp_listener_transport();

    /**
     * @brief Last packet reception info.
     * @return A const reference to **packet_info** related to the last received packet.
     */
    const packet_info_type& info() const;
    /**
     * @brief Closes this udp listener transport.
     */
    void close();

    /**
     * @brief Non-copy assignable.
     */
    udp_listener_transport& operator=(const udp_listener_transport&) = delete;

private:
    using allocation_guard_type = boost::memory::allocation_guard<allocator>;

    static constexpr size_t control_buffer_size = 1024;

    template <typename ip_traits_e, typename allocator_e>
    friend std::ostream& operator<< (
            std::ostream &os,
            const udp_listener_transport<ip_traits_e, allocator_e>& tr);

    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher& dispatcher_;
    udp_options options_;

    std::vector<address_type> groups_;
    uint16_t port_;

    address_type interface_;

    receive_callback_type receive_callback_;

    allocator allocator_;
    allocation_guard_type control_buffer_guard_;
    allocation_guard_type recv_buffer_guard_;

    receive_buffer_type control_buffer_;
    receive_buffer_type recv_buffer_;
    packet_info_type info_;

};

}

#include "udp_listener_transport.ipp"

