// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "atomic.hpp"
#include "spsc_fixed_circular_buffer.hpp"

#include <boost/utils/traits/callable_traits.hpp>

#include <cmath>


namespace boost { namespace concurrency {

template <typename Element, typename Mixin>
inline spsc_fixed_circular_buffer<Element, Mixin>::spsc_fixed_circular_buffer(std::size_t capacity)
        :
    Base(capacity)
{
    if (Mixin::MIXIN_ENABLED)
    {
        auto validStart = Base::valid_start_.read_volatile();
        auto validEnd = Base::valid_end_.read_volatile();

        Mixin::after_created(validStart, validEnd);

        Base::valid_start_.put_fenced(validStart);
        Base::valid_end_.put_fenced(validEnd);
    }
}

template <typename Element, typename Mixin>
inline spsc_fixed_circular_buffer<Element, Mixin>::~spsc_fixed_circular_buffer()
{

}

template <typename Element, typename Mixin>
template <typename Callback>
bool spsc_fixed_circular_buffer<Element, Mixin>::push(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(Element&)>::value,
            "Callback has to be a callable void(Element&)");
    
    if (Mixin::MIXIN_ENABLED)
    {
        Mixin::before_push(
                Base::valid_start_.read_dirty(), 
                Base::valid_end_.read_dirty());
    }

    std::size_t currentEnd = Base::valid_end_.read_dirty();
    std::size_t nextEnd = (currentEnd + 1) & Base::capacity_mask_;
    if (nextEnd == Base::valid_start_.read_fenced())
    {
//        if (Mixin::MIXIN_ENABLED)
//            Mixin::AfterPush(ReadValidStart(), ReadValidEnd(), nullptr);

        return false;
    }
    else
    {
        Element& element = *(reinterpret_cast<Element*>(Base::data_) + currentEnd);
        callback(element);

        Base::valid_end_.put_fenced(nextEnd);

        if (Mixin::MIXIN_ENABLED)
        {
            Mixin::after_push(
                    Base::valid_start_.read_dirty(), 
                    Base::valid_end_.read_dirty(), 
                    &element);
        }

        return true;
    }
}

template <typename Element, typename Mixin>
template <typename Callback>
bool spsc_fixed_circular_buffer<Element, Mixin>::consume(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(const Element&)>::value
         || utils::is_callable<Callback, bool(const Element&)>::value,
            "Callback has to be a callable void/bool(const Element&)");
    
    if (Mixin::MIXIN_ENABLED)
    {
        Mixin::before_consume(
                Base::valid_start_.read_dirty(), 
                Base::valid_end_.read_dirty());
    }

    auto currentStart = Base::valid_start_.read_dirty();
    auto currentEnd = Base::valid_end_.read_fenced();

    if (currentStart == currentEnd)
    {
        if (Mixin::MIXIN_ENABLED)
        {
            Mixin::after_consume(
                    Base::valid_start_.read_dirty(), 
                    Base::valid_end_.read_dirty());
        }

        return false;
    }
    else
    {
        do
        {
            auto& element = *(reinterpret_cast<Element*>(Base::data_) + currentStart);
            auto should_continue = utils::call_with_bool_return(callback, element);
            if (!should_continue)
                break;

            currentStart = (currentStart + 1) & Base::capacity_mask_;
        }
        while (currentStart != currentEnd);
        Base::valid_start_.put_fenced(currentStart);

        if (Mixin::MIXIN_ENABLED)
        {
            Mixin::after_consume(
                    Base::valid_start_.read_dirty(), 
                    Base::valid_end_.read_dirty());
        }

        return true;
    }
}

} }

