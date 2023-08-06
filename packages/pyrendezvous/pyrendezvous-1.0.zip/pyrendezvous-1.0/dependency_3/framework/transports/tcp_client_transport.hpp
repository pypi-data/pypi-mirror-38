#pragma once

#include <framework/dispatcher.hpp>
#include <framework/transports/options/tcp_options.hpp>
#include <framework/transports/transport.hpp>

#include <boost/concurrency/field.hpp>
#include <boost/memory.hpp>

#include <condition_variable>
#include <functional>
#include <mutex>


namespace framework {

/**
 * @brief Provides client connection for TCP network services
 *
 * @details
 * @para
 * **tcp_client_transport** provides facilities for async interaction with a TCP server.
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
 *
 * framework::dispatcher dispatcher;
 * framework::loop main_loop(dispatcher);
 *
 * framework::tcp_options options;
 * framework::ipv4_tcp_client::single_sender::client_transport transport(
 *       dispatcher,
 *       options,
 *       "time.nist.gov:13",
 *       [](auto& source)
 *       {
 *           cout << "connected!" << endl;
 *       },
 *       [](auto& source)
 *       {
 *           cout << "disconnected!" << endl;
 *       },
 *       [](auto& source, auto& buffer)
 *       {
 *           cout << buffer.length() << endl;
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
 */
template <typename ip_traits, typename send_buffer, typename allocator = boost::memory::mallocator>
class tcp_client_transport final : public transport
{
public:
    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    using transport_type = tcp_client_transport<ip_traits, send_buffer, allocator>;
    using connected_callback_type = std::function<void(tcp_client_transport&)>;
    using disconnected_callback_type = std::function<void(tcp_client_transport&)>;
    using receive_buffer_type = boost::memory::buffer_ref;
    using receive_callback_type = std::function<void(transport_type&, receive_buffer_type&)>;
    using send_buffer_type = send_buffer;
    using bool_field_type = boost::concurrency::field<size_t>;

    /**
     * @brief Initializes a new instance of **tcp_client_transport**.
     * @param dispatcher A dispatcher this transport will be registered with.
     * @param options TCP socket customization options.
     * @param endpoint Remote endpoint this transport will try to connect with.
     * @param connected_callback A callback invoked whenever the connection is established.
     * @param disconnected_callback A callback invoked whenever an established connection is finished.
     * @param receive_callback A callback invoked upon reception of data from remote host.
     * @param error_callback A callback invoked upon errors raised from within the transport.
     */
    explicit tcp_client_transport(
            dispatcher& dispatcher,
            tcp_options options,
            endpoint_type endpoint,
            connected_callback_type connected_callback,
            disconnected_callback_type disconnected_callback,
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Non-copy constructable.
     */
    tcp_client_transport(const tcp_client_transport&) = delete;

    /**
     * @brief Destroys **tcp_client_transport**.
     */
    ~tcp_client_transport();

    /**
     * @brief Indicates if the connection to the remote host is active.
     *
     * @details
     * A connection is in **connected** state after connected and before disconnected
     * callbacks are invoked.
     * @return **true** if the transport's connection to the remote host is active,
     * **false** otherwise.
     */
    bool is_connected() const;
    /**
     * @brief Indicates if there are any datagrams in the ring buffer awaiting sent.
     * @returns True if there are datagrams awaiting sent, False otherwise.
     */
    bool has_pending() const;

    /**
     * @brief Sends chunk of data over TCP to a remote host.
     *
     * @details
     * @para
     * This is a non-blocking operation. This means that an attempt is made to send data using underlying socket,
     * however if the socket os not ready the data is temporarily stored in underlying ring buffer and send when
     * the socket is ready.
     *
     * @param data The data to send.
     * @tparam data_type Type of data to send.
     * @returns True if data was sent or stored in the ring buffer, False otherwise.
     */
    template <typename data_type>
    bool send(const data_type& data);
    /**
     * @brief Disconnects the client.
     * @details
     * A call to this method doesnot close the underlying socket and dispatch
     * **disconnected_callback** immediately. Instead a request to close the connection
     * is placed on the I/O queue and will be dispatched as any other event
     * by related **dispatcher**.
     */
    void disconnect();
    /**
     * @brief Closes the transport.
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
    tcp_client_transport& operator=(const tcp_client_transport&) = delete;

private:
    using allocation_guard_type = boost::memory::allocation_guard<allocator>;

    template <typename ip_traits_e, typename send_buffer_e, typename allocator_e>
    friend std::ostream& operator<<(
            std::ostream& os,
            const tcp_client_transport<ip_traits_e, send_buffer_e, allocator_e>& tr);

    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher& dispatcher_;
    tcp_options options_;
    endpoint_type endpoint_;

    connected_callback_type connected_callback_;
    disconnected_callback_type disconnected_callback_;
    receive_callback_type receive_callback_;
    error_callback_type error_callback_;

    allocator allocator_;
    allocation_guard_type recv_buffer_guard_;
    receive_buffer_type recv_buffer_;
    send_buffer_type send_buffer_;

    bool is_connected_{false};
    bool is_disconnected_{false};

    std::mutex all_sent_mutex_;
    std::condition_variable all_sent_;

};

}

/**
 * An example how to write a tcp client with **tcp_client_transport**:
 *
 * @example framework/transports/tcp_client_transport.cpp
 */

#include "tcp_client_transport.ipp"

