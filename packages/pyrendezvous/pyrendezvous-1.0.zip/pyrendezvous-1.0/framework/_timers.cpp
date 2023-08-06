#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>
#include <framework/timers.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>
#include <pybind11/nonable_function.hpp>

#include <chrono>

using namespace std;
using namespace std::chrono;
using namespace framework;

namespace py = pybind11;

using nonable_error_callback = py::nonable_function<framework::rendezvous_error&>;


PYBIND11_MODULE(_timers, m)
{
    py::class_<one_shot_timer>(m, "OneShotTimer")
            .def(py::init<dispatcher&, py::function, nonable_error_callback>(),
                    py::arg("dispatcher"),
                    py::arg("elapsed_callback"),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def_property_readonly("is_armed",
                    (bool(one_shot_timer::*)())&framework::timer::is_armed)
            .def("schedule", &one_shot_timer::schedule<microseconds::rep, microseconds::period>,
                    py::arg("interval"))
            .def("disarm",
                    (void(one_shot_timer::*)())&framework::timer::disarm);

    py::class_<auto_reload_timer>(m, "AutoReloadTimer")
            .def(py::init<dispatcher&, microseconds, py::function, nonable_error_callback>(),
                    py::arg("dispatcher"),
                    py::arg("interval"),
                    py::arg("elapsed_callback"),
                    py::arg("error_callback") = nullptr,
                    py::keep_alive<1, 2>())
            .def("arm", &auto_reload_timer::arm)
            .def("disarm",
                    (void(auto_reload_timer::*)())&framework::timer::disarm)
            .def_property_readonly("is_armed",
                    (bool(auto_reload_timer::*)())&framework::timer::is_armed);
}


