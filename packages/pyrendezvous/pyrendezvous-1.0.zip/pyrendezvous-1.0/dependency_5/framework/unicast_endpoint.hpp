#pragma once

#include <framework/transports.hpp>
#include <pybind11/pybind11.h>

#include <sstream>
#include <string>


namespace unicast_endpoint {
    
static const auto endpoint_tuple_size = 2;
static const auto address_index = 0;
static const auto port_index = 1;

bool try_endpoint_string(pybind11::object obj, std::string& address_and_port)
{
    if (!pybind11::isinstance<pybind11::str>(obj))
        return false;

    address_and_port.clear();
    address_and_port.append(obj.cast<std::string>());
    return true;
}

bool try_endpoint_tuple(pybind11::object obj, std::string& address, uint16_t& port)
{
    if (!pybind11::isinstance<pybind11::tuple>(obj))
        return false;

    pybind11::tuple candidate = obj;
    if (candidate.size() != endpoint_tuple_size)
        return false;

    pybind11::object address_candidate = candidate[address_index];
    pybind11::object port_candidate = candidate[port_index];

    if (!pybind11::isinstance<pybind11::str>(address_candidate) || !pybind11::isinstance<pybind11::int_>(port_candidate))
        return false;

    address = address_candidate.cast<std::string>();
    port = port_candidate.cast<uint16_t>();
    return true;
}

template <typename endpoint_type>
pybind11::tuple endpoint_to_tuple(endpoint_type&& endpoint)
{
    pybind11::tuple candidate(endpoint_tuple_size);

    std::stringstream address;
    address << endpoint.get_address();

    candidate[address_index] = address.str();
    candidate[port_index] = endpoint.get_port();

    return candidate;
}
    
}

