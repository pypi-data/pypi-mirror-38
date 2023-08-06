#pragma once

#include <framework/dispatcher.hpp>
#include <framework/transports/options/tcp_options.hpp>
#include <framework/transports/packet_info.hpp>
#include <framework/transports/transport.hpp>

#include <boost/any.hpp>
#include <boost/concurrency/field.hpp>
#include <boost/memory.hpp>
#include <boost/optional.hpp>

#include <condition_variable>
#include <functional>
#include <iostream>
#include <list>
#include <mutex>


namespace framework {

/**
 * @brief Listens for connections from TCP network clients.
 *
 * @details
 * @para
 * **tcp_server_transport** binds to a local endpoint and listens to incoming tcp
 * connection requests in async way. A newly created **tcp_server_transport** starts
 * listening immediately. An accepted connection is reported to client code
 * through a registered callback. For each accepted connection a new, independent
 * **connected_client_transport** is created. This models a unique connection with
 * accepted client. Upon data reception and disconnection **connected_client_transport**
 * raises appropriate callbacks.
 *
 * @para
 * The following code example creates a **tcp_server_transport** and accepts
 * the connection from a client:
 * @code
 * #include <framework/dispatcher.hpp>
 * #include <framework/loop.hpp>
 * #include <framework/transports.hpp>
 * ...
 * framework::dispatcher dispatcher;
 *
 * framework::tcp_options options;
 * framework::ipv4_tcp_server::single_sender::server_transport transport(
 *      dispatcher,
 *      options,
 *      "0.0.0.0:27000",
 *      [](auto& connected_client)
 *      {
 *          cout << connected_client << " connected!" << endl;
 *      },
 *      [](auto& disconnected_client)
 *      {
 *          cout << disconnected_client << " disconnected!" << endl;
 *      },
 *      [](auto& connected_client, auto& buffer)
 *      {
 *          cout << "received " << buffer.length() << " bytes from " << connected_client << endl;
 *      },
 *      [](auto& error)
 *      {
 *          cerr << error.what() << endl;
 *      });
 * ...
 * @endcode
 *
 * @tparam ip_traits
 * @tparam send_buffer
 */
template <typename ip_traits, typename send_buffer, typename allocator = boost::memory::mallocator>
class tcp_server_transport final : public transport
{
public:
    class connected_client_transport;

    using address_type = typename ip_traits::address_type;
    using endpoint_type = typename ip_traits::endpoint_type;
    using transport_type = tcp_server_transport<ip_traits, send_buffer>;
    using connected_callback_type = std::function<void(connected_client_transport&)>;
    using disconnected_callback_type = std::function<void(connected_client_transport&)>;
    using receive_buffer_type = boost::memory::buffer_ref;
    using receive_callback_type = std::function<void(connected_client_transport&, receive_buffer_type&)>;

    /**
     * @brief Represents an active TCP connection from a client.
     *
     * @details
     * @para
     * Whenever an incoming connection request is accepted an instance of this type is
     * created to model that connection. An instance of **connected_client_transport**
     * is reported to client code through connected callback. It's a reposibility of
     * the client to capture a reference to the transport from that point and use it for sending
     * data to connected client for the duration of the connection with that client.
     *
     * @para
     * The following code example creates a **tcp_server_transport** and accepts
     * the connection from a client:
     * @code
     * #include <framework/dispatcher.hpp>
     * #include <framework/loop.hpp>
     * #include <framework/transports.hpp>
     * ...
     * framework::dispatcher dispatcher;
     * std::list<server_transport::connected_client_transport> connected_transports;
     *
     * framework::tcp_options options;
     * framework::ipv4_tcp_server::single_sender::server_transport transport(
     *      dispatcher,
     *      options,
     *      "0.0.0.0:27000",
     *      [&connected_transports](auto& connected_client)
     *      {
     *          cout << connected_client << " connected!" << endl;
     *          connected_clients.push_back(connected_client);
     *      },
     *      [](auto& disconnected_client)
     *      {
     *          cout << disconnected_client << " disconnected!" << endl;
     *          connected_clients.remove(connected_client);
     *      },
     *      [](auto& connected_client, auto& buffer)
     *      {
     *          cout << "received " << buffer.length() << " bytes from " << connected_client << endl;
     *      },
     *      [](auto& error)
     *      {
     *          cerr << error.what() << endl;
     *      });
     * ...
     * @endcode
     */
    class connected_client_transport final : public transport
    {
    public:
        using transport_type = tcp_server_transport<ip_traits, send_buffer, allocator>::connected_client_transport;
        using disconnected_callback_type = std::function<void(transport_type&)>;
        using packet_info_type = packet_info<ip_traits>;
        using receive_buffer_type = boost::memory::buffer_ref;
        using receive_callback_type = std::function<void(connected_client_transport&, receive_buffer_type&)>;
        using error_callback_type = transport::error_callback_type;
        using send_buffer_type = send_buffer;
        using bool_field_type = boost::concurrency::field<size_t>;

        /**
         * @brief Initializes a new **connected_client_transport**.
         * @details
         * Connected client transport represents a TCP tunnel between server and client identified by a pair of
         * endpoints. Each endpoint has it's unique address and port.
         *
         * @param dispatcher A dispatcher for asynchronous dispatch of message queue related to this transport.
         * @param socketfd A file descriptor of the underlying socket.
         * @param server_endpoint
         * @param client_endpoint
         * @param options
         * @param disconnected_callback
         * @param receive_callback
         * @param error_callback
         */
        explicit connected_client_transport(
                dispatcher& dispatcher,
                int socketfd,
                allocator& alloc,
                endpoint_type server_endpoint,
                endpoint_type client_endpoint,
                tcp_options options,
                disconnected_callback_type disconnected_callback,
                receive_callback_type receive_callback,
                error_callback_type error_callback = {});
        /**
         * @brief Non-copy constructable.
         */
        connected_client_transport(const connected_client_transport&) = delete;

        /**
         * @brief Destructor.
         */
        ~connected_client_transport();

        /**
         * @brief Gets **connected_client_transport** id.
         * @details
         * This id is guaranteed to be unique only among client transports produced by the same **tcp_server_transport**.
         *
         * @return Transport id.
         */
        int id() const;
        /**
         * @brief Gets connected client endpoint.
         * @return Client address and port of connected transport.
         */
        endpoint_type from() const;
        /**
         * @brief Indicates if there are any datagrams in the ring buffer awaiting sent.
         * @returns True if there are datagrams awaiting sent, False otherwise.
         */
        bool has_pending() const;
        /**
         * @brief Info about last reception.
         * @return Packet reception info.
         */
        const packet_info_type& info() const;
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
         * @brief Gets closure data associated with this transport.
         * @details
         * @paragraph
         * @details
         * When client is connected, user can specify closure data. The transport neither examines nor
         * modifies the closure. Instead it presents the same point in the event callbacks related to that transport.
         *
         * @details
         * Unless pointer to user closure has been specified with **set_closure** this method will return **boost::none**.
         *
         * @details
         * If **closure_type** doesn't match type provided with **set_closure**, **boost::bad_any_cast** will be thrown.
         *
         * @tparam closure_type Closure type.
         * @return **boost::none** or reference to closure.
         */
        template <typename closure_type>
        boost::optional<closure_type&> closure();
        /**
         * @brief Associates closure data to this transport.
         * @details
         * @paragraph
         * When client is connected, user can supply closure data rvalue. The transport neither examines nor
         * modifies the closure. Instead it presents the data in every event callbacks related to that transport
         *
         * @paragraph
         * Lifetime of the closure will be equal to the transport or another closure assignment to the same transport.
         *
         * @tparam closure_type Closure type.
         * @param pointer A pointer to allocated closure.
         */
        template <typename closure_type>
        void set_closure(closure_type&& closure);
        /**
         * @brief Associates a pointer to closure data to this transport.
         * @details
         * @paragraph
         * When client is connected, user can supply a pointer closure data. The transport neither examines nor
         * modifies the closure. Instead it presents the pointer  in every event callbacks related to that transport
         *
         * @paragraph
         * User should ensure alignment of closure and transport lifetimes.
         *
         * @tparam closure_type Closure type.
         * @param pointer A pointer to allocated closure.
         */
        template <typename closure_type>
        void set_closure(closure_type* pointer);

        /**
         * @brief Sends given data over TCP conenction or schedules for send if underlying socket isnt ready.
         * @param data Chunk of data to send.
         * @tparam data_type Type of data to send
         * @return True if data was successfully sent or stored in internal buffer for later send, False otherwise.
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
         * @brief Does exactly the same as **disconnect**.
         * @details
         * This is a trait method for all connection and connection-less transports.
         */
        void close();
        /**
         * @brief Waits for pending sends.
         * @details
         * All send operations implemented within this buffer are fully async.
         * It means that after placing data on ring buffer send method immediately
         * returns to client code. The actual send happens when socket is ready
         * and an appropriate send event is dispatched through I/O queue. In such case
         * the only way to determine completness of send process is to monitor
         * the state of the underlying buffer. This method waits until all the data
         * from the underlying ring buffer is successfully sent.
         *
         * @param timeout Wait timeout duration.
         * @return true if there is no more pending data for send, flase if wait timeout
         * has been reached and there is still some pending data in the buffer.
         */
        template <typename rep, typename period>
        bool wait(std::chrono::duration<rep, period> timeout);

        /**
         * @brief Checks quality between two connected client transports.
         * @details
         * Two connected client transports are considered to be equal if they share the same socket.
         *
         * @param other Other **connected_client_transport** to compare with.
         * @return True if transports are equal, false otherwise.
         */
        bool operator==(const connected_client_transport& other) const;
        /**
         * @brief Checks less than relation between two transports.
         * @details
         * @paragraph
         * This operator is used by default implementation of **std::less** algorithm, which in tern is used to define
         * relation between elements in a **std::set**. Having less than operator implemented, **connected_client_transport**
         * can be used as an element of a set.
         *
         * @paragraph
         * Relation less than between instances of **connected_client_transport** is translated directly to equivalent relation
         * between their socket descriptiors (numbers).
         *
         * @return True if this client has socket descriptor lower than the **other**.
         */
        bool operator<(const connected_client_transport& other) const;

        /**
         * @brief Non-copy assignable.
         */
        connected_client_transport& operator=(const connected_client_transport&) = delete;

    private:
        using allocation_guard_type = boost::memory::allocation_guard<allocator>;

        friend std::ostream& operator<<(std::ostream& os, const transport_type& tr)
        {
            os << "tcp:" << tr.client_endpoint_ << "[" << tr.server_endpoint_ << "]";
            return os;
        }

        virtual void handle_event(
                bool should_receive,
                bool should_send,
                bool should_disconnect) override;

        int id_;
        endpoint_type server_endpoint_;
        endpoint_type client_endpoint_;

        dispatcher& dispatcher_;
        tcp_options options_;

        disconnected_callback_type disconnected_callback_;
        receive_callback_type receive_callback_;

        allocation_guard_type recv_buffer_guard_;
        receive_buffer_type recv_buffer_;
        packet_info_type info_;
        send_buffer_type send_buffer_;

        bool is_disconnected_{false};
        bool is_connected_{true};

        std::mutex all_sent_mutex_;
        std::condition_variable all_sent_;

        boost::any closure_;

    };

    /**
     * @brief Creates an instance of tcp server listening client connections.
     * @details
     * @para
     * The **endpoint** has to be a valid endpoint along to the **ip_traits** used.
     * As such it has to consist of address : port. If given port is 0, an unused
     * port will be assigned by the system. Later the complete endpoint definition
     * can be retrieved witt **at**.
     *
     * @para
     * Whenever a new client is connected **connected_callback** is invoked.
     * Transport passed in the callback defines a unique pipe between server and
     * the client. This transport can be used outside of the scope of the callback.
     * Whenever client transport is disconnected, either by client or server,
     * **disconnected_callback** is invoked. All client transports will be deallocated
     * after this callback. Thus in case client code keeps reference to any client
     * transports, it should react on **disconnect_callback** and removed all references.
     *
     * @param dispatcher A **dispatcher** to register the server with.
     * @param options TCP options for this server.
     * @param endpoint An endpoint at which the server should listen.
     * @param connected_callback A callback invoked when a new client connection is
     * established.
     * @param disconnected_callback A callback invoked on client connection close,
     * just before client connection object is deallocated.
     * @param receive_callback A callback invoked whenever data is received from a client.
     * This callback may be invoked by multiple client transports, the actual originator
     * is passed as an invocation argument.
     * @param error_callback A callback invoked whenever an error is detected.
     */
    explicit tcp_server_transport(
            dispatcher& dispatcher,
            tcp_options options,
            endpoint_type endpoint,
            connected_callback_type connected_callback,
            disconnected_callback_type disconnected_callback,
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Destructor.
     */
    ~tcp_server_transport();

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
     * @brief Closes the underlying socket.
     */
    void close();

    /**
     * @brief Non-copy constructable.
     */
    tcp_server_transport(const tcp_server_transport&) = delete;
    /**
     * @brief Non-copy assignable.
     */
    tcp_server_transport& operator=(const tcp_server_transport&) = delete;

private:
    friend std::ostream& operator<<(std::ostream& os, const transport_type& tr)
    {
        os << "tcp:" << tr.endpoint_;
        return os;
    }

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
    std::list<connected_client_transport> connected_clients_;
};

}

/**
 * An example how to write a tcp server with **tcp_server_transport**:
 *
 * @example framework/transports/tcp_server_transport.cpp
 */

#include "tcp_server_transport.ipp"

