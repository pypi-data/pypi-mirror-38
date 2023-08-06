// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "fixed_circular_buffer.hpp"
#include "field.hpp"

#include <boost/utils/traits/callable_traits.hpp>

#include <cmath>


namespace boost { namespace concurrency {

template <typename Element>
inline fixed_circular_buffer<Element>::fixed_circular_buffer(std::size_t capacity)
        :
    capacity_(round_pow_2(capacity)),
    capacity_mask_(capacity_ - 1ul),
    data_length_(sizeof(Element) * capacity_),
    data_(new std::uint8_t[sizeof(Element) * capacity_])
{

}

template <typename Element>
inline fixed_circular_buffer<Element>::~fixed_circular_buffer()
{
    delete[] data_;
}

template <typename Element>
inline std::size_t fixed_circular_buffer<Element>::count() const
{
    return (valid_end_.read_fenced() - valid_start_.read_fenced()) & capacity_mask_;
}

template <typename Element>
inline Element* fixed_circular_buffer<Element>::operator [](std::size_t index)
{
    if (index < count())
    {
        auto position = (valid_start_.read_volatile() + index) % capacity_;
        return (reinterpret_cast<Element*>(data_) + position);
    }
    else
    {
        return nullptr;
    }
}

template <typename Element>
inline std::size_t fixed_circular_buffer<Element>::round_pow_2(std::size_t x)
{
    return pow(2, ceil(::log(x)/::log(2)));
}

} }

