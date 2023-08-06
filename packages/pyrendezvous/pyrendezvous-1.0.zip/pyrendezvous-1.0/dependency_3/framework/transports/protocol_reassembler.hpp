#pragma once

#include <boost/memory.hpp>

#include <functional>
#include <limits>


namespace framework {

/**
 * @brief Reconstructs messages from a stream.
 *
 * @details
 * @para
 * Application level message boundaries aren't preserved during delivery over stream
 * protocols such as TCP. This is a reactive component which can be registered in a place of
 * a **receive_callback** with any tcp transport. Upon a reception of TCP data it will
 * attempt to reconstruct full application level messages from partial buffers reported by
 * the transport. Whenever a message is completely reconstructed a callback will notify
 * client code about the reception handing over a reference to reconstructed message.
 *
 * @para
 * This type has been implemented as a functor. It means it can be invoked with a
 * signature given by it's **operator()** and can be registered as a valid callback handler.
 *
 * @para
 * This reassembler requires a **protocol trait** to recognise reassembled message.
 * The trait shall provide a single static method **complete_size**. This method
 * provided with a **buffer_ref** shall detemine size of the next complete message in that buffer.
 * In case the buffer doesn't contain complete message the method should return 0.
 *
 * @para
 * Sample protocol trait definition:
 * @code
 * ...
 *
 * struct soup_header
 * {
 *      uint16_t packet_length_;
 *      char packet_type_;
 * };
 *
 * struct debug : soup_header
 * {
 *      static const char identifier = '+';
 *
 *      char text_[0];
 * };
 *
 * struct login_accepted : soup_header
 * {
 *      static const char identifier = 'A';
 *
 *      char session_[10];
 *      char sequence_number_[20];
 * };
 *
 * struct login_rejected : soup_header
 * {
 *      static const char identifier = 'J';
 *
 *      char reject_reason_code_;
 * };
 *
 * struct sequenced_data : soup_header
 * {
 *      static const char identifier = 'S';
 *
 *      char message_[0];
 * };
 *
 * struct souptcp_traits
 * {
 *      static const size_t unfinished = 0ul;
 *
 *      inline static size_t complete_size(framework::buffer_ref&& buffer)
 *      {
 *          if (buffer.length() < sizeof(soup_header))
 *              return unfinished;
 *
 *          auto& header = buffer.as<soup_header&>();
 *          return header.packet_length_;
 *      }
 * };
 *
 * ...
 * @endcode
 *
 * Sample usage with **tcp_client_transport**:
 * @code
 * #include <framework/transports/protocol_reassembler.hpp>
 * ...
 *
 * framework::ipv4_tcp_client::single_sender::client_transport transport(
 *      dispatcher,
 *      options,
 *      "time.nist.gov:13",
 *      [](auto& source)
 *      {
 *          cout << "connected!" << endl;
 *      },
 *      [](auto& source)
 *      {
 *          cout << "disconnected!" << endl;
 *      },
 *      framework::protocol_reassembler<decltype(transport), souptcp_traits>(
 *              [](auto& source, framework::buffer_ref& buffer)
 *              {
 *                  auto& header = buffer.as<soup_header&>();
 *                  cout << "message:" << header.packet_type_ << " length:" << buffer.length() << endl;
 *              }),
 *      [](auto& error)
 *      {
 *          cerr << error.what() << endl;
 *      });
 *
 * ...
 * @endcode
 *
 * @tparam source_type A type of transport from which the source event came from.
 * This parameter is used to transpass event source to the reassembled callback.
 * @tparam protocol_traits A type providing information about reconstructed protocol.
 * This type is required to provide a single static method **complete_size** taking
 * **buffer_ref** as a parameter.
 * @tparam partial_limit Determines maximum number of bytes allocated for storing 
 * partial messages. 
 */
template <
        typename source_type, 
        typename protocol_traits,
        size_t partial_limit=std::numeric_limits<size_t>::max()>
class protocol_reassembler
{
public:
    /**
     * @brief Callback invoked with reconstructed messages.
     */
    using callback_type = std::function<void(source_type&, boost::memory::buffer_ref& message)>;

    /**
     * @breif Creates an instance of the reassembler with a callback.
     *
     * @details
     * The **callback** will be invoked whenever a complete message is reconstruted
     * according to the type traits.
     * @param callback The callback to be invoked when a message is reconstructed.
     */
    explicit protocol_reassembler(callback_type callback);

    /**
     * @brief Forwards execution to this functor.
     *
     * @param source A source of this callback.
     * @param buffer A buffer to reassemble messages from.
     */
    void operator()(source_type& source, boost::memory::buffer_ref& buffer);
    
    /**
     * @brief Forwards execution to this functor.
     *
     * @param source A source of this callback.
     * @param buffer A buffer to reassemble messages from.
     */
    void operator()(source_type& source, boost::memory::buffer_ref&& buffer);

    /**
     * @brief Determines if a partial message is stored within the reassembler.
     *
     * @details
     * Buffers received through **operator()** may contain incomplete application
     * level messages. A message isn't reported through the callback unless it has been
     * reassembled completely. This method determines if reassembler holds a part of
     * a message in its internal buffers witing for the rest of the message to be delivered
     * with subsequent invocations of **operator()**.
     * @return true if incomplete message is hold by the reassembler, false otherwise.
     */
    bool unfinished() const;

private:
    class partial
    {
    public:
        partial();
        ~partial();

        void append(void* data, size_t length);
        void reset();

        size_t length() const;

        boost::memory::buffer_ref operator*() const;

    private:
        static const size_t initial_capacity = 4096;

        void* data_;
        size_t capacity_;
        size_t position_{0ul};
    };

    callback_type callback_;
    partial partial_;
};

/**
 * A sample reassembler for [soup tcp protocol](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/soupbintcp.pdf).
 *
 * @example framework/transports/souptcp_reassembler.cpp
 */

}

#include "protocol_reassembler.ipp"

