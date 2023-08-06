// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "atomic.hpp"
#include "mpsc_fixed_circular_buffer.hpp"

#include <boost/utils/traits/callable_traits.hpp>

#include <cmath>

namespace boost { namespace concurrency {

template <typename Element, typename Mixin>
inline mpsc_fixed_circular_buffer<Element, Mixin>::mpsc_fixed_circular_buffer(std::size_t capacity)
        :
    Base(capacity)
{
    if (Mixin::MIXIN_ENABLED)
    {
        auto valid_start = Base::valid_start_.read_volatile();
        auto valid_end = Base::valid_end_.read_volatile();
        auto claimed_end = claimed_end_.read_volatile();

        Mixin::after_created(valid_start, valid_end, claimed_end);

        Base::valid_start_.put_fenced(valid_start);
        Base::valid_end_.put_fenced(valid_end);
        claimed_end_.put_fenced(claimed_end);
    }
}

template <typename Element, typename Mixin>
inline mpsc_fixed_circular_buffer<Element, Mixin>::~mpsc_fixed_circular_buffer()
{
    
}

template <typename Element, typename Mixin>
template <typename Callback>
bool mpsc_fixed_circular_buffer<Element, Mixin>::push(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(Element&)>::value,
            "Callback has to be a callable");
    
    if (Mixin::MIXIN_ENABLED)
    {
        Mixin::before_push(
                Base::valid_start_.read_dirty(),
                Base::valid_end_.read_dirty(),
                claimed_end_.read_dirty());
    }

    auto current_start = Base::valid_start_.read_dirty();
    auto current_claimed = claimed_end_.read_dirty();
    load_fence();

    auto next_claimed = (current_claimed + 1) & Base::capacity_mask_;
    if (next_claimed == current_start)
    {
        if (Mixin::MIXIN_ENABLED)
        {
            Mixin::after_push(
                    Base::valid_start_.read_dirty(),
                    Base::valid_end_.read_dirty(),
                    claimed_end_.read_dirty());
        }

        return false;
    }

    if (!claimed_end_.compare_exchange(current_claimed, next_claimed))
        return false;

    auto& element = *(reinterpret_cast<Element*>(Base::data_) + current_claimed);
    callback(element);

    while(!Base::valid_end_.compare_exchange(current_claimed, next_claimed))
    {
        if (Mixin::MIXIN_ENABLED)
        {
            auto valid_start = Base::valid_start_.read_volatile();
            auto valid_end = Base::valid_end_.read_volatile();
            auto claimed_end = claimed_end_.read_volatile();

            Mixin::failed_commit(
                    valid_start,
                    valid_end,
                    claimed_end);

            Base::valid_start_.put_fenced(valid_start);
            Base::valid_end_.put_fenced(valid_end);
            claimed_end_.put_fenced(claimed_end);
        }
    }

    if (Mixin::MIXIN_ENABLED)
    {
        Mixin::after_push(
                Base::valid_start_.read_dirty(),
                Base::valid_end_.read_dirty(),
                claimed_end_.read_dirty());
    }

    return true;
}

template <typename Element, typename Mixin>
template <typename Callback>
bool mpsc_fixed_circular_buffer<Element, Mixin>::consume(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(const Element&)>::value
         || utils::is_callable<Callback, bool(const Element&)>::value,
            "Callback has to be a callable void(const Element&)");
    
    if (Mixin::MIXIN_ENABLED)
    {
        Mixin::before_consume(
                Base::valid_start_.read_dirty(),
                Base::valid_end_.read_dirty());
    }

    auto current_start = Base::valid_start_.read_dirty();
    auto current_end = Base::valid_end_.read_fenced();

    if (current_start == current_end)
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
            const auto& element = *(reinterpret_cast<Element*>(Base::data_) + current_start);
            auto should_continue = utils::call_with_bool_return(callback, element);
            if (!should_continue)
                break;

            current_start = (current_start + 1) & Base::capacity_mask_;
        }
        while (current_start != current_end);
        Base::valid_start_.put_fenced(current_start);

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

