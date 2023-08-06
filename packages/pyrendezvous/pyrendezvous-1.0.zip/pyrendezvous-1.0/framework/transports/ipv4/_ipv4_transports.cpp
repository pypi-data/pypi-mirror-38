#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>
#include <framework/transports.hpp>

#include <framework/unicast_endpoint.hpp>
#include <framework/multicast_endpoint.hpp>

#include <boost/memory.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>
#include <pybind11/nonable_function.hpp>
#include <pybind11/return_policy.hpp>

#include <chrono>
#include <cstring>
#include <sstream>
#include <string>
#include <vector>

#include <unistd.h>
#include <fcntl.h>

using namespace std;
using namespace std::chrono;
using namespace boost::memory;
using namespace framework;

namespace py = pybind11;

using ipv4_address = framework::ip::v4::address;
using ipv4_endpoint = framework::ip::v4::endpoint;
using ipv4_packet_info = framework::packet_info<framework::ip::v4::traits>;
using ipv4_udp_listener_transport = framework::ipv4_udp::listener_transport;
using ipv4_udp_publisher_transport = framework::ipv4_udp::single_sender::publisher_transport;
using ipv4_tcp_client_transport = framework::ipv4_tcp_client::single_sender::client_transport;
using ipv4_tcp_server_transport = framework::ipv4_tcp_server::single_sender::server_transport;
using ipv4_tcp_connected_client_transport = framework::ipv4_tcp_server::single_sender::server_transport::connected_client_transport;
using ipv4_udp_client_transport = framework::ipv4_udp::single_sender::client_transport;
using ipv4_udp_server_transport = framework::ipv4_udp::single_sender::server_transport;

using nonable_error_callback = py::nonable_function<framework::rendezvous_error&>;


struct packet_info_helper
{
    static py::tuple origin(ipv4_packet_info& self)
    {
        return unicast_endpoint::endpoint_to_tuple(self.from());
    }
};

template <typename transport_type>
struct dispatchable_helper
{
    static bool __bool__(transport_type& self)
    {
        static const auto fcntl_error = -1;

        auto result = fcntl(self.fd(), F_GETFL);
        return result != fcntl_error;
    }
};

template <typename transport_type>
struct transport_helper : dispatchable_helper<transport_type>
{
    static py::object __enter__(py::object self)
    {
        return self;
    }

    static void __exit__(
            transport_type& self,
            py::object exc_type,
            py::object exc_value,
            py::object traceback)
    {
        self.close();
    }

    static std::string __str__(transport_type& self)
    {
        stringstream description;
        description << self;

        return description.str();
    }

    static bool send(transport_type& self, py::object data)
    {
        if (py::isinstance<py::buffer>(data))
        {
            py::buffer buffer = data;
            py::buffer_info info = buffer.request(false);
            return self.send(buffer_ref(info.ptr, info.size * info.itemsize));
        }
        else if (py::isinstance<py::str>(data))
        {
            auto characters = data.cast<std::string>();
            return self.send(buffer_ref(characters.data(), characters.length()));
        }

        throw py::type_error("unsupported data type!");
    }
};

template <typename transport_type>
struct ipv4_udp_transport_helper : transport_helper<transport_type>
{

};

struct ipv4_udp_listener_transport_helper : ipv4_udp_transport_helper<ipv4_udp_listener_transport>
{
    static void create(
            ipv4_udp_listener_transport& self,
            dispatcher& dispatcher,
            py::object groups,
            py::function receive_callback,
            py::str interface,
            udp_options& options,
            nonable_error_callback error_callback)
    {
        // try to get the group as a string "<address>:<port>"
        {
            std::string group;
            if (multicast_endpoint::try_group_string(groups, group))
            {
                new (&self) ipv4_udp_listener_transport(
                    dispatcher,
                    options,
                    group,
                    interface.cast<std::string>(),
                    receive_callback,
                    error_callback);

                return;
            }
        }

        // try to get the group as a tuple (address, port)
        {
            std::string address;
            uint16_t port;
            if (multicast_endpoint::try_group_tuple(groups, address, port))
            {
                new (&self) ipv4_udp_listener_transport(
                        dispatcher,
                        options,
                        { address, port },
                        interface.cast<std::string>(),
                        receive_callback,
                        error_callback);

                return;
            }
        }

        // try groups as touple of list of addresses and port ([address1, address2 .. ], port)
        {
            vector<ipv4_address> addresses;
            uint16_t port;
            if (multicast_endpoint::try_groups_tuple(groups, addresses, port))
            {
                new (&self) ipv4_udp_listener_transport(
                        dispatcher,
                        options,
                        move(addresses),
                        port,
                        interface.cast<std::string>(),
                        receive_callback,
                        error_callback);

                return;
            }
        }

        throw py::type_error("wrong group definition!");
    }
};

struct ipv4_udp_publisher_transport_helper : ipv4_udp_transport_helper<ipv4_udp_publisher_transport>
{
    static void create(
            ipv4_udp_publisher_transport& self,
            dispatcher& dispatcher,
            py::object group,
            py::str interface,
            udp_options options,
            nonable_error_callback error_callback)
    {
        // try to get the group as a string "<address>:<port>"
        {
            std::string address_and_port;
            if (multicast_endpoint::try_group_string(group, address_and_port))
            {
                new (&self) ipv4_udp_publisher_transport(
                    dispatcher,
                    options,
                    address_and_port,
                    interface.cast<std::string>(),
                    error_callback);

                return;
            }
        }

        // try to get the group as a tuple (address, port)
        {
            std::string address;
            uint16_t port;
            if (multicast_endpoint::try_group_tuple(group, address, port))
            {
                new (&self) ipv4_udp_publisher_transport(
                        dispatcher,
                        options,
                        { address, port },
                        interface.cast<std::string>(),
                        error_callback);

                return;
            }
        }

        throw py::type_error("wrong group definition!");
    }
};

template <typename transport_type>
struct ipv4_tcp_transport_helper : transport_helper<transport_type>
{
    static py::tuple from(transport_type& self)
    {
        return unicast_endpoint::endpoint_to_tuple(self.from());
    }
};

struct ipv4_tcp_client_transport_helper : ipv4_tcp_transport_helper<ipv4_tcp_client_transport>
{
    static void create(
            ipv4_tcp_client_transport& self,
            dispatcher& dispatcher,
            py::object endpoint,
            py::function connected_callback,
            py::function disconnected_callback,
            py::function receive_callback,
            tcp_options options,
            nonable_error_callback error_callback)
    {
        // endpoint as a string
        {
            std::string address_and_port;
            if (unicast_endpoint::try_endpoint_string(endpoint, address_and_port))
            {
                new (&self) ipv4_tcp_client_transport(
                        dispatcher,
                        options,
                        address_and_port,
                        connected_callback,
                        disconnected_callback,
                        receive_callback,
                        error_callback);

                return;
            }
        }

        // endpoint as a tuple
        {
            std::string address;
            uint16_t port;
            if (unicast_endpoint::try_endpoint_tuple(endpoint, address, port))
            {
                new (&self) ipv4_tcp_client_transport(
                        dispatcher,
                        options,
                        { address, port },
                        connected_callback,
                        disconnected_callback,
                        receive_callback,
                        error_callback);

                return;
            }
        }

        // unsupported endpoint type
        throw py::type_error("unsupported endpoint type!");
    }

    static bool __bool__(ipv4_tcp_client_transport& self)
    {
        return dispatchable_helper<ipv4_tcp_client_transport>::__bool__(self) && self.is_connected();
    }
};

struct ipv4_tcp_server_transport_helper : ipv4_tcp_transport_helper<ipv4_tcp_server_transport>
{
    static void create(
            ipv4_tcp_server_transport& self,
            dispatcher& dispatcher,
            py::object endpoint,
            py::function connected_callback,
            py::function disconnected_callback,
            py::function receive_callback,
            tcp_options options,
            nonable_error_callback error_callback)
    {
        // endpoint as a string
        {
            std::string address_and_port;
            if (unicast_endpoint::try_endpoint_string(endpoint, address_and_port))
            {
                new (&self) ipv4_tcp_server_transport(
                        dispatcher,
                        options,
                        address_and_port,
                        py::set_reference_return_policy(connected_callback),
                        py::set_reference_return_policy(disconnected_callback),
                        py::set_reference_return_policy(receive_callback),
                        error_callback);

                return;
            }
        }

        // endpoint as a tuple
        {
            std::string address;
            uint16_t port;
            if (unicast_endpoint::try_endpoint_tuple(endpoint, address, port))
            {
                new (&self) ipv4_tcp_server_transport(
                        dispatcher,
                        options,
                        { address, port },
                        py::set_reference_return_policy(connected_callback),
                        py::set_reference_return_policy(disconnected_callback),
                        py::set_reference_return_policy(receive_callback),
                        error_callback);

                return;
            }
        }

        // unsupported endpoint type
        throw py::type_error("unsupported endpoint type!");
    }

    static py::tuple at(ipv4_tcp_server_transport& self)
    {
        return unicast_endpoint::endpoint_to_tuple(self.at());
    }
};

struct ipv4_tcp_connected_client_transport_helper : ipv4_tcp_transport_helper<ipv4_tcp_connected_client_transport>
{
    static py::object get_closure(ipv4_tcp_connected_client_transport& self)
    {
        auto closure = self.closure<py::object>();
        if (!closure)
            return py::none();

        return *closure;
    }

    static void set_closure(ipv4_tcp_connected_client_transport& self, py::object closure)
    {
        self.set_closure(closure);
    }

    static bool __bool__(ipv4_tcp_connected_client_transport& self)
    {
        return dispatchable_helper<ipv4_tcp_connected_client_transport>::__bool__(self) && self.is_connected();
    }
};

struct ipv4_udp_client_transport_helper : ipv4_udp_transport_helper<ipv4_udp_client_transport>
{
    static void create(
            ipv4_udp_client_transport& self,
            dispatcher& dispatcher,
            py::object endpoint,
            py::function receive_callback,
            udp_options& options,
            nonable_error_callback error_callback)
    {
        // endpoint as a string
        {
            std::string address_and_port;
            if (unicast_endpoint::try_endpoint_string(endpoint, address_and_port))
            {
                new (&self) ipv4_udp_client_transport(
                        dispatcher,
                        options,
                        address_and_port,
                        py::set_reference_return_policy(receive_callback),
                        error_callback);

                return;
            }
        }

        // endpoint as a tuple
        {
            std::string address;
            uint16_t port;
            if (unicast_endpoint::try_endpoint_tuple(endpoint, address, port))
            {
                new (&self) ipv4_udp_client_transport(
                        dispatcher,
                        options,
                        { address, port },
                        py::set_reference_return_policy(receive_callback),
                        error_callback);

                return;
            }
        }

        // unsupported endpoint type
        throw py::type_error("unsupported endpoint type!");
    }
};

struct ipv4_udp_server_transport_helper : ipv4_udp_transport_helper<ipv4_udp_server_transport>
{
    static void create(
            ipv4_udp_server_transport& self,
            dispatcher& dispatcher,
            py::object endpoint,
            py::function receive_callback,
            udp_options& options,
            nonable_error_callback error_callback)
    {
        // endpoint as a string
        {
            std::string address_and_port;
            if (unicast_endpoint::try_endpoint_string(endpoint, address_and_port))
            {
                new (&self) ipv4_udp_server_transport(
                        dispatcher,
                        options,
                        address_and_port,
                        py::set_reference_return_policy(receive_callback),
                        error_callback);

                return;
            }
        }

        // endpoint as a tuple
        {
            std::string address;
            uint16_t port;
            if (unicast_endpoint::try_endpoint_tuple(endpoint, address, port))
            {
                new (&self) ipv4_udp_server_transport(
                        dispatcher,
                        options,
                        { address, port },
                        py::set_reference_return_policy(receive_callback),
                        error_callback);

                return;
            }
        }

        // unsupported endpoint type
        throw py::type_error("unsupported endpoint type!");
    }

    static py::tuple at(ipv4_tcp_server_transport& self)
    {
        return unicast_endpoint::endpoint_to_tuple(self.at());
    }

    static bool reply(ipv4_udp_server_transport& self, py::object data)
    {
        if (py::isinstance<py::buffer>(data))
        {
            py::buffer buffer = data;
            py::buffer_info info = buffer.request(false);
            return self.reply(buffer_ref(info.ptr, info.size * info.itemsize));
        }
        else if (py::isinstance<py::str>(data))
        {
            auto characters = data.cast<std::string>();
            return self.reply(buffer_ref(characters.data(), characters.length()));
        }

        throw py::type_error("unsupported data type!");
    }
};

PYBIND11_MODULE(_ipv4_transports, m)
{
    // register attributes
    stringstream default_interface;
    default_interface << ipv4_address::any();

    m.attr("DEFAULT_INTERFACE") = default_interface.str();
    m.attr("LOOPBACK_INTERFACE") = "127.0.0.1";

    // register classes
    py::class_<buffer_ref>(m, "BufferRef", py::buffer_protocol())
            .def_buffer(
                [](buffer_ref& instance) -> py::buffer_info
                {
                    return py::buffer_info(
                            instance.as_pointer<void*>(),
                            sizeof(uint8_t),
                            py::format_descriptor<uint8_t>::format(),
                            instance.length());
                })
            .def("__len__", &buffer_ref::length)
            .def("subbuf", &buffer_ref::subbuf,
                    py::arg("length"));

    py::class_<ipv4_packet_info>(m, "PacketInfo")
            .def_property_readonly("origin", &packet_info_helper::origin)
            .def_property_readonly("receive_time", &ipv4_packet_info::receive_time)
            .def_property_readonly("read_time", &ipv4_packet_info::read_time)
            .def("since", &ipv4_packet_info::since);

    py::class_<ipv4_udp_listener_transport>(m, "UdpListenerTransport")
            .def("__init__", &ipv4_udp_listener_transport_helper::create,
                    py::arg("dispatcher"),
                    py::arg("groups"),
                    py::arg("receive_callback"),
                    py::arg("interface") = default_interface.str(),
                    py::arg("options") = udp_options(),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("info", &ipv4_udp_listener_transport::info)
            .def("__bool__", &ipv4_udp_listener_transport_helper::__bool__)
            .def("__enter__", &ipv4_udp_listener_transport_helper::__enter__)
            .def("__exit__", &ipv4_udp_listener_transport_helper::__exit__)
            .def("__str__", &ipv4_udp_listener_transport_helper::__str__);

    py::class_<ipv4_udp_publisher_transport>(m, "UdpPublisherTransport")
            .def("__init__", &ipv4_udp_publisher_transport_helper::create,
                    py::arg("dispatcher"),
                    py::arg("groups"),
                    py::arg("interface") = default_interface.str(),
                    py::arg("options") = udp_options(),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("has_pending", &ipv4_udp_publisher_transport::has_pending)
            .def("send", &ipv4_udp_publisher_transport_helper::send,
                    py::arg("data"))
            .def("wait", &ipv4_udp_publisher_transport::wait<microseconds::rep, microseconds::period>)
            .def("__bool__", &ipv4_udp_publisher_transport_helper::__bool__)
            .def("__enter__", &ipv4_udp_publisher_transport_helper::__enter__)
            .def("__exit__", &ipv4_udp_publisher_transport_helper::__exit__)
            .def("__str__", &ipv4_udp_publisher_transport_helper::__str__);

    py::class_<ipv4_tcp_client_transport>(m, "TcpClientTransport")
            .def("__init__", &ipv4_tcp_client_transport_helper::create,
                    py::arg("dispatcher"),
                    py::arg("endpoint"),
                    py::arg("connected_callback"),
                    py::arg("disconnected_callback"),
                    py::arg("receive_callback"),
                    py::arg("options") = tcp_options(),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("has_pending", &ipv4_tcp_client_transport::has_pending)
            .def("send", &ipv4_tcp_client_transport_helper::send,
                    py::arg("data"))
            .def("wait", &ipv4_tcp_client_transport::wait<microseconds::rep, microseconds::period>)
            .def("disconnect", &ipv4_tcp_client_transport::disconnect)
            .def("__bool__", &ipv4_tcp_client_transport_helper::__bool__)
            .def("__enter__", &ipv4_tcp_client_transport_helper::__enter__)
            .def("__exit__", &ipv4_tcp_client_transport_helper::__exit__)
            .def("__str__", &ipv4_tcp_client_transport_helper::__str__);

    py::class_<ipv4_tcp_server_transport>(m, "TcpServerTransport")
            .def("__init__", &ipv4_tcp_server_transport_helper::create,
                    py::arg("dispatcher"),
                    py::arg("endpoint"),
                    py::arg("connected_callback"),
                    py::arg("disconnected_callback"),
                    py::arg("receive_callback"),
                    py::arg("options") = tcp_options(),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("at", &ipv4_tcp_server_transport_helper::at)
            .def("__bool__", &ipv4_tcp_server_transport_helper::__bool__)
            .def("__enter__", &ipv4_tcp_server_transport_helper::__enter__)
            .def("__exit__", &ipv4_tcp_server_transport_helper::__exit__)
            .def("__str__", &ipv4_tcp_server_transport_helper::__str__);

    py::class_<ipv4_tcp_connected_client_transport>(m, "TcpConnectedClientTransport")
            .def_property_readonly("id", &ipv4_tcp_connected_client_transport::id)
            .def_property_readonly("info", &ipv4_tcp_connected_client_transport::info)
            .def_property_readonly("has_pending", &ipv4_tcp_connected_client_transport::has_pending)
            .def_property("closure",
                    &ipv4_tcp_connected_client_transport_helper::get_closure,
                    &ipv4_tcp_connected_client_transport_helper::set_closure)
            .def("send", &ipv4_tcp_connected_client_transport_helper::send,
                    py::arg("data"))
            .def("wait", &ipv4_tcp_connected_client_transport::wait<microseconds::rep, microseconds::period>)
            .def("disconnect", &ipv4_tcp_connected_client_transport::disconnect)
            .def("__bool__", &ipv4_tcp_connected_client_transport_helper::__bool__)
            .def("__str__", &ipv4_tcp_connected_client_transport_helper::__str__);

    py::class_<ipv4_udp_client_transport>(m, "UdpClientTransport")
            .def("__init__", &ipv4_udp_client_transport_helper::create,
                    py::arg("dispatcher"),
                    py::arg("endpoint"),
                    py::arg("receive_callback"),
                    py::arg("options") = udp_options(),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("info", &ipv4_udp_client_transport::info)
            .def_property_readonly("has_pending", &ipv4_udp_client_transport::has_pending)
            .def("send", &ipv4_udp_client_transport_helper::send,
                    py::arg("data"))
            .def("wait", &ipv4_udp_client_transport::wait<microseconds::rep, microseconds::period>)
            .def("__bool__", &ipv4_udp_client_transport_helper::__bool__)
            .def("__enter__", &ipv4_udp_client_transport_helper::__enter__)
            .def("__exit__", &ipv4_udp_client_transport_helper::__exit__)
            .def("__str__", &ipv4_udp_client_transport_helper::__str__);

    py::class_<ipv4_udp_server_transport>(m, "UdpServerTransport")
            .def("__init__", &ipv4_udp_server_transport_helper::create,
                    py::arg("dispatcher"),
                    py::arg("endpoint"),
                    py::arg("receive_callback"),
                    py::arg("options") = udp_options(),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("at", &ipv4_udp_server_transport_helper::at)
            .def_property_readonly("has_pending", &ipv4_udp_server_transport::has_pending)
            .def("reply", &ipv4_udp_server_transport_helper::reply,
                    py::arg("data"))
            .def("wait", &ipv4_udp_server_transport::wait<microseconds::rep, microseconds::period>)
            .def("__bool__", &ipv4_udp_server_transport_helper::__bool__)
            .def("__enter__", &ipv4_udp_server_transport_helper::__enter__)
            .def("__exit__", &ipv4_udp_server_transport_helper::__exit__)
            .def("__str__", &ipv4_udp_server_transport_helper::__str__);
}