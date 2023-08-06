#pragma once

#include <framework/transports/options/tcp_options.hpp>
#include <framework/transports/options/udp_options.hpp>

#include <framework/transports/network/ipv4.hpp>

#include <framework/transports/transport.hpp>
#include <framework/transports/tcp_server_transport.hpp>
#include <framework/transports/tcp_client_transport.hpp>
#include <framework/transports/udp_listener_transport.hpp>
#include <framework/transports/udp_publisher_transport.hpp>
#include <framework/transports/udp_server_transport.hpp>
#include <framework/transports/udp_client_transport.hpp>

#include <boost/concurrency.hpp>


namespace framework {

using ipv4_traits = ip::v4::traits;

using spsc_ring_buffer = boost::concurrency::spsc_variable_circular_buffer<>;
using mpsc_ring_buffer = boost::concurrency::mpsc_variable_circular_buffer<>;

namespace ipv4_udp {
 
using listener_transport = udp_listener_transport<ipv4_traits>;

namespace single_sender {

using publisher_transport = udp_publisher_transport<ipv4_traits, spsc_ring_buffer>;
using server_transport = udp_server_transport<ipv4_traits, spsc_ring_buffer>;
using client_transport = udp_client_transport<ipv4_traits, spsc_ring_buffer>;

}

namespace multiple_senders {

using publisher_transport = udp_publisher_transport<ipv4_traits, mpsc_ring_buffer>;
using server_transport = udp_server_transport<ipv4_traits, mpsc_ring_buffer>;
using client_transport = udp_client_transport<ipv4_traits, mpsc_ring_buffer>;

}
}

namespace ipv4_tcp_server {
namespace single_sender {

using server_transport = tcp_server_transport<ipv4_traits, spsc_ring_buffer>;
using client_transport = server_transport::connected_client_transport;

}

namespace multiple_senders {
using server_transport = tcp_server_transport<ipv4_traits, mpsc_ring_buffer>;
using connected_client_transport = server_transport::connected_client_transport;

}
}

namespace ipv4_tcp_client {
namespace single_sender {

using client_transport = tcp_client_transport<ipv4_traits, spsc_ring_buffer>;

}

namespace multiple_senders {

using client_transport = tcp_client_transport<ipv4_traits, mpsc_ring_buffer>;

}
}

}

