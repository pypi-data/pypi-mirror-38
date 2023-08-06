#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>
#include <framework/loop.hpp>
#include <framework/transports.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>
#include <pybind11/nonable_function.hpp>

#include <chrono>

using namespace std;
using namespace std::chrono;
using namespace framework;

namespace py = pybind11;

using nonable_error_callback = py::nonable_function<framework::rendezvous_error&>;


struct dispatcher_helper
{
    static void __init__(dispatcher& self, nonable_error_callback error_callback, py::object parent)
    {
        if (parent.is_none())
            new (&self) framework::dispatcher(error_callback);
        else
        {
            auto& parent_dispatcher = parent.cast<framework::dispatcher&>();
            new (&self) framework::dispatcher(parent_dispatcher, error_callback);
        }
    }

    static bool dispatch(dispatcher& self, py::object timeout)
    {
        if (timeout.is_none())
            return self.dispatch();
        else
        {
            auto timeout_us = timeout.cast<microseconds>();
            return self.dispatch(duration_cast<milliseconds>(timeout_us));
        }
    }
};

PYBIND11_MODULE(_framework, m)
{
    py::class_<rendezvous_error>(m, "RendezvousError")
            .def("where", &rendezvous_error::where);

    py::class_<dispatcher>(m, "Dispatcher")
            .def("__init__", &dispatcher_helper::__init__,
                    py::arg("error_callback") = nullptr,
                    py::arg("parent") = nullptr,
                    py::keep_alive<1, 3>())
            .def("dispatch", &dispatcher_helper::dispatch,
                    py::arg("timeout") = nullptr);

    py::class_<loop>(m, "Loop")
            .def(py::init<dispatcher&>())
            .def("run_forever", &loop::run_forever)
            .def("interrupt", &loop::interrupt)
            .def("interrupt_on", &loop::interrupt_on,
                    py::arg("signo"));
}

