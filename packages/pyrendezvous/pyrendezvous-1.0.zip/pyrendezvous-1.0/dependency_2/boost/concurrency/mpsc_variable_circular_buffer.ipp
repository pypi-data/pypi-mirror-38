// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "variable_circular_buffer.hpp"

#include <boost/utils/traits/callable_traits.hpp>


namespace boost { namespace concurrency {

template <typename Mixin>
inline mpsc_variable_circular_buffer<Mixin>::mpsc_variable_circular_buffer(std::string shmKey, std::size_t capacity)
        :
    variable_circular_buffer(shmKey, capacity)
{
    if (Mixin::MIXIN_ENABLED)
    {
        auto valid_start = valid_start_.read_volatile();
        auto valid_end = valid_end_.read_volatile();
        auto claimed_end = claimed_end_.read_volatile();

        Mixin::after_created(
                valid_start,
                valid_end,
                claimed_end,
                Base::first_map_);

        valid_start_.put_fenced(valid_start);
        valid_end_.put_fenced(valid_end);
        claimed_end_.put_fenced(claimed_end);
    }
}

template <typename Mixin>
inline mpsc_variable_circular_buffer<Mixin>::mpsc_variable_circular_buffer(std::size_t capacity)
        :
    variable_circular_buffer(capacity)
{
    if (Mixin::MIXIN_ENABLED)
    {
        auto valid_start = valid_start_.read_volatile();
        auto valid_end = valid_end_.read_volatile();
        auto claimed_end = claimed_end_.read_volatile();

        Mixin::after_created(
                valid_start,
                valid_end,
                claimed_end,
                Base::first_map_);

        valid_start_.put_fenced(valid_start);
        valid_end_.put_fenced(valid_end);
        claimed_end_.put_fenced(claimed_end);
    }
}

template <typename Mixin>
inline mpsc_variable_circular_buffer<Mixin>::~mpsc_variable_circular_buffer()
{
}

template <typename Mixin>
template <typename Callback>
inline bool mpsc_variable_circular_buffer<Mixin>::push(const Callback& callback, std::size_t size)
{
    static_assert(
            utils::is_callable<Callback, void(uint8_t*)>::value,
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
    thread_fence();

    auto distance = Base::distance(current_claimed, current_start);
    if (distance < Base::record_size(size) + 1)
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

    auto next_claimed = (current_claimed + Base::record_size(size)) % Base::capacity_;
    if (!claimed_end_.compare_exchange(current_claimed, next_claimed))
        return false;

    auto length = reinterpret_cast<std::size_t*>(Base::first_map_ + current_claimed);
    *length = size;

    auto data = reinterpret_cast<std::uint8_t*>(Base::first_map_ + current_claimed + sizeof(std::size_t));
    callback(data);

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

template <typename Mixin>
template <typename Callback>
inline bool mpsc_variable_circular_buffer<Mixin>::consume(const Callback& callback)
{
    static_assert(
            utils::is_callable<Callback, void(const std::uint8_t*, std::size_t)>::value
         || utils::is_callable<Callback, bool(const std::uint8_t*, std::size_t)>::value,
            "Callback has to be a callable void/bool(std::uint8_t*, std::size_t)");
    
    if (Mixin::MIXIN_ENABLED)
    {
        Mixin::before_consume(
                Base::valid_start_.read_dirty(),
                Base::valid_end_.read_dirty());
    }

    auto current_start_ = Base::valid_start_.read_dirty();
    auto current_end_ = Base::valid_end_.read_fenced();

    if (current_start_ == current_end_)
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
            auto length = reinterpret_cast<std::size_t*>(Base::first_map_ + current_start_);
            const auto data = Base::first_map_ + current_start_ + sizeof(std::size_t);
            auto should_continue = utils::call_with_bool_return(callback, data, *length);
            if (!should_continue)
                break;

            current_start_ = (current_start_ + Base::record_size(*length)) % Base::capacity_;
        }
        while (current_start_ != current_end_);
        Base::valid_start_.put_fenced(current_start_);

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

