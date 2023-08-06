#include <framework/transports.hpp>

#include <pybind11/pybind11.h>

using namespace std;
using namespace framework;

namespace py = pybind11;


struct udp_options_helper
{
    static void __init__(udp_options& self, py::kwargs args)
    {
        static constexpr auto read_buffer_size_key = "read_buffer_size";
        static constexpr auto send_buffer_size_key = "send_buffer_size";
        static constexpr auto sp_rcvbuf_key = "sp_rcvbuf";
        static constexpr auto sp_sndbuf_key = "sp_sndbuf";
        static constexpr auto loop_key = "loop";
        static constexpr auto ttl_key = "ttl";
        static constexpr auto timestampns_key = "timestampns";
        static constexpr auto pktinfo_key = "pktinfo";

        static constexpr auto pop_method = "pop";

        auto arg_pop = args.attr(pop_method);
        auto read_buffer_size = arg_pop(read_buffer_size_key, py::none());
        if (!read_buffer_size.is_none())
            self.read_buffer_size = read_buffer_size.cast<size_t>();

        auto send_buffer_size = arg_pop(send_buffer_size_key, py::none());
        if (!send_buffer_size.is_none())
            self.send_buffer_size = send_buffer_size.cast<size_t>();

        auto sp_rcvbuf = arg_pop(sp_rcvbuf_key, py::none());
        if (!sp_rcvbuf.is_none())
            self.sp_rcvbuf = sp_rcvbuf.cast<size_t>();

        auto sp_sndbuf = arg_pop(sp_sndbuf_key, py::none());
        if (!sp_sndbuf.is_none())
            self.sp_sndbuf = sp_sndbuf.cast<size_t>();

        auto loop = arg_pop(loop_key, py::none());
        if (!loop.is_none())
            self.loop = loop.cast<bool>();

        auto ttl = arg_pop(ttl_key, py::none());
        if (!ttl.is_none())
            self.ttl = ttl.cast<uint8_t>();

        auto timestampns = arg_pop(timestampns_key, py::none());
        if (!timestampns.is_none())
            self.timestampns = timestampns.cast<bool>();

        auto pktinfo = arg_pop(pktinfo_key, py::none());
        if (!pktinfo.is_none())
            self.pktinfo = pktinfo.cast<bool>();

        if (py::len(args) > 0)
            throw py::value_error("unknown parameters!");
    }
};

struct tcp_options_helper
{
    static void __init__(tcp_options& self, py::kwargs args)
    {
        static constexpr auto read_buffer_size_key = "read_buffer_size";
        static constexpr auto send_buffer_size_key = "send_buffer_size";
        static constexpr auto sp_rcvbuf_key = "sp_rcvbuf";
        static constexpr auto sp_sndbuf_key = "sp_sndbuf";
        static constexpr auto listen_backlog_key = "listen_backlog";
        static constexpr auto no_delay_key = "no_delay";
        static constexpr auto quick_ack_key = "quick_ack";

        static constexpr auto pop_method = "pop";

        auto arg_pop = args.attr(pop_method);
        auto read_buffer_size = arg_pop(read_buffer_size_key, py::none());
        if (!read_buffer_size.is_none())
            self.read_buffer_size = read_buffer_size.cast<size_t>();

        auto send_buffer_size = arg_pop(send_buffer_size_key, py::none());
        if (!send_buffer_size.is_none())
            self.send_buffer_size = send_buffer_size.cast<size_t>();

        auto sp_rcvbuf = arg_pop(sp_rcvbuf_key, py::none());
        if (!sp_rcvbuf.is_none())
            self.sp_rcvbuf = sp_rcvbuf.cast<size_t>();

        auto sp_sndbuf = arg_pop(sp_sndbuf_key, py::none());
        if (!sp_sndbuf.is_none())
            self.sp_sndbuf = sp_sndbuf.cast<size_t>();

        auto listen_backlog = arg_pop(listen_backlog_key, py::none());
        if (!listen_backlog.is_none())
            self.listen_backlog = listen_backlog.cast<size_t>();

        auto no_delay = arg_pop(no_delay_key, py::none());
        if (!no_delay.is_none())
            self.no_delay = no_delay.cast<bool>();

        auto quick_ack = arg_pop(quick_ack_key, py::none());
        if (!quick_ack.is_none())
            self.quick_ack = quick_ack.cast<bool>();

        if (py::len(args) > 0)
            throw py::value_error("unknown parameters!");
    }
};

PYBIND11_MODULE(_options, m)
{
    py::class_<udp_options>(m, "UdpOptions")
            .def("__init__", &udp_options_helper::__init__)
            .def_readwrite("read_buffer_size", &udp_options::read_buffer_size)
            .def_readwrite("send_buffer_size", &udp_options::send_buffer_size)
            .def_readwrite("sp_rcvbuf", &udp_options::sp_rcvbuf)
            .def_readwrite("sp_sndbuf", &udp_options::sp_sndbuf)
            .def_readwrite("loop", &udp_options::loop)
            .def_readwrite("ttl", &udp_options::ttl)
            .def_readwrite("timestampns", &udp_options::timestampns)
            .def_readwrite("pktinfo", &udp_options::pktinfo);

    py::class_<tcp_options>(m, "TcpOptions")
            .def("__init__", &tcp_options_helper::__init__)
            .def_readwrite("read_buffer_size", &tcp_options::read_buffer_size)
            .def_readwrite("send_buffer_size", &tcp_options::send_buffer_size)
            .def_readwrite("sp_rcvbuf", &tcp_options::sp_rcvbuf)
            .def_readwrite("sp_sndbuf", &tcp_options::sp_sndbuf)
            .def_readwrite("listen_backlog", &tcp_options::listen_backlog)
            .def_readwrite("no_delay", &tcp_options::no_delay)
            .def_readwrite("quick_ack", &tcp_options::quick_ack);
}

