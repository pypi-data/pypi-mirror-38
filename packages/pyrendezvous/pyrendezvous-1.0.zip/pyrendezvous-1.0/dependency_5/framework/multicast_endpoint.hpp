#pragma once

#include <framework/transports.hpp>
#include <pybind11/pybind11.h>

#include <string>
#include <vector>


namespace multicast_endpoint {
    
static const auto group_tuple_size = 2;
static const auto address_index = 0;
static const auto port_index = 1;

bool try_group_string(pybind11::object obj, std::string& group)
{
    if (!pybind11::isinstance<pybind11::str>(obj))
        return false;

    group.clear();
    group.append(obj.cast<std::string>());
    return true;
}

bool try_group_tuple(pybind11::object obj, std::string& address, uint16_t& port)
{
    if (!pybind11::isinstance<pybind11::tuple>(obj))
        return false;

    pybind11::tuple candidate = obj;
    if (candidate.size() != group_tuple_size)
        return false;

    pybind11::object candidate_address = candidate[address_index];
    pybind11::object candidate_port = candidate[port_index];
    if (!pybind11::isinstance<pybind11::str>(candidate_address) || !pybind11::isinstance<pybind11::int_>(candidate_port))
        return false;

    address.clear();
    address.append(candidate_address.cast<std::string>());
    port = candidate_port.cast<uint16_t>();
    return true;
}

template <typename address_type>
bool try_groups_tuple(
        pybind11::object obj, 
        std::vector<address_type>& addresses, 
        uint16_t& port)
{
    if (!pybind11::isinstance<pybind11::tuple>(obj))
        return false;

    pybind11::tuple candidate = obj;
    pybind11::object candidate_list = candidate[address_index];
    pybind11::object candidate_port = candidate[port_index];

    if (!pybind11::isinstance<pybind11::list>(candidate_list) || !pybind11::isinstance<pybind11::int_>(candidate_port))
        return false;

    pybind11::list candidate_addresses = candidate_list;
    for (auto candidate_address : candidate_addresses)
    {
        if (!pybind11::isinstance<pybind11::str>(candidate_address))
            return false;

        address_type address(candidate_address.cast<std::string>());
        addresses.push_back(address);
    }

    port = candidate_port.cast<uint16_t>();
    return true;
}

}

