// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "fixed_circular_buffer.hpp"

#include <boost/utils/traits/callable_traits.hpp>


namespace boost { namespace concurrency {

template <typename Element, typename Mixin>
inline unsafe_fixed_circular_buffer<Element, Mixin>::unsafe_fixed_circular_buffer(std::size_t capacity)
        :
    data_(new std::uint8_t[sizeof(Element) * capacity]),
    data_length_(sizeof(Element) * capacity),
    data_owner_(true),
    capacity_(capacity)
{
    Mixin::after_created(valid_start_, valid_end_);
}

template <typename Element, typename Mixin>
inline unsafe_fixed_circular_buffer<Element, Mixin>::unsafe_fixed_circular_buffer(std::uint8_t* data, std::size_t length)
        :
    data_(data),
    data_length_(length),
    data_owner_(false),
    capacity_(length / sizeof(Element))
{
    Mixin::after_created(valid_start_, valid_end_);
}

template <typename Element, typename Mixin>
inline unsafe_fixed_circular_buffer<Element, Mixin>::~unsafe_fixed_circular_buffer()
{
    if (data_owner_)
        delete[] data_;
}

template <typename Element, typename Mixin>
template <typename Callback>
bool unsafe_fixed_circular_buffer<Element, Mixin>::push(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(Element&)>::value,
            "Callback has to be a callable");
    
    Mixin::before_push(valid_start_, valid_end_);

    auto next_end = (valid_end_ + 1) % capacity_;
    if (next_end == valid_start_)
    {
        Mixin::after_push(valid_start_, valid_end_, nullptr);
        return false;
    }
    else
    {
        auto& element = *(reinterpret_cast<Element*>(data_) + valid_end_);
        callback(element);

        valid_end_ = next_end;

        Mixin::after_push(valid_start_, valid_end_, &element);
        return true;
    }
}

template <typename Element, typename Mixin>
template <typename Callback>
bool unsafe_fixed_circular_buffer<Element, Mixin>::consume(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(const Element&)>::value,
            "Callback has to be a callable void(Element&)");
    
    Mixin::before_consume(valid_start_, valid_end_);
    if (valid_start_ == valid_end_)
    {
        Mixin::after_consume(valid_start_, valid_end_);
        return false;
    }
    else
    {
        const auto& element = *(reinterpret_cast<Element*>(data_) + valid_start_);
        callback(element);

        valid_start_ = (valid_start_ + 1) % capacity_;

        Mixin::after_consume(valid_start_, valid_end_);
        return true;
    }
}

template <typename Element, typename Mixin>
inline std::size_t unsafe_fixed_circular_buffer<Element, Mixin>::count() const
{
    return (valid_end_ - valid_start_) % capacity_;
}

template <typename Element, typename Mixin>
inline Element* unsafe_fixed_circular_buffer<Element, Mixin>::operator [](std::size_t index)
{
    if (index < count())
    {
        auto position = (valid_start_ + index) % capacity_;
        return (reinterpret_cast<Element*>(data_) + position);
    }
    else
    {
        return nullptr;
    }
}

} }

