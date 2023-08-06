#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>
#include <framework/signals/signal_handler.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/nonable_function.hpp>

using namespace std;
using namespace framework;

namespace py = pybind11;

using nonable_error_callback = py::nonable_function<framework::rendezvous_error&>;


PYBIND11_MODULE(_signals, m)
{
    py::class_<signal_handler>(m, "SignalHandler")
            .def(py::init<dispatcher&, int, py::function, nonable_error_callback>(),
                    py::arg("dispatcher"),
                    py::arg("signo"),
                    py::arg("receive_callback"),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>());
}
