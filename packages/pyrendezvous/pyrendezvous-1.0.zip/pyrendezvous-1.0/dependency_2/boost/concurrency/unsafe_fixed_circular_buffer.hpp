// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include <cstddef>
#include <cstdint>

namespace boost { namespace concurrency { 
   
/**
 * @brief A void mixin for **unsafe_fixed_circular_buffer**.
 * 
 * @details
 * Provides an empty [mixin](http://www.drdobbs.com/cpp/mixin-based-programming-in-c/184404445) 
 * for **spsc_fixed_circular_buffer**. The intention is to have it completely optimized 
 * out during release compilation, so in-depth look at the buffer won't affect performance.
 */
class unsafe_fixed_circular_buffer_no_mixin
{
protected:
    void after_created(
        std::size_t& validStart, 
        std::size_t& validEnd) 
    { }
    
    void before_push(
            std::size_t validStart, 
            std::size_t validEnd) 
    { }
    template <typename Element>
    void after_push(
            std::size_t validStart, 
            std::size_t validEnd, 
            Element* pushed) 
    { }
    
    void before_consume(
            std::size_t validStart, 
            std::size_t validEnd) 
    { }
    void after_consume(
            std::size_t validStart, 
            std::size_t validEnd) 
    { }
};

/**
 * @brief A thread unsafe circular buffer with fixed size elements.
 * 
 * @details
 * @para
 * This type acts as a general purpose collection for storing elements in a 
 * [ring buffer](https://en.wikipedia.org/wiki/Circular_buffer).
 * 
 * @tparam Mixin
 */
template <typename Element, typename Mixin=unsafe_fixed_circular_buffer_no_mixin>    
class unsafe_fixed_circular_buffer : public Mixin
{
public:
    /**
     * @brief Creates a circular buffer with the given capacity.
     * @param capacity The desired capacity of the buffer.
     */
    unsafe_fixed_circular_buffer(std::size_t capacity);
    /**
     * @brief Creates a circular buffer using preallocated memory.
     * @param data The preallocated buffer to use.
     * @param length The length of the preallocated memory buffer.
     */
    unsafe_fixed_circular_buffer(std::uint8_t* data, std::size_t length);
    /**
     * @brief Releases related resources.
     */
    ~unsafe_fixed_circular_buffer();
    
    /**
     * @brief Pushes an element onto the buffer.
     * @param callback A callback invoked for each published element.
     * @return **true** if publication was successful, **false** if there's 
     * no space left in the buffer.
     */
    template <typename Callback>
    bool push(const Callback& callback);
    
    /**
     * @brief Consumes elements from the buffer.
     * @param callback A callback invoked for each subsequently consumed element.
     * @return **true** if one or more elements were consumed, **false** otherwise.
     */
    template <typename Callback>
    bool consume(const Callback& callback);
    
    /**
     * @brief Counts number of elements ready for consumption.
     * @return Number of elements ready for consumption.
     */
    std::size_t count() const;
    /**
     * 
     * @param index
     * @return 
     */
    Element* operator [](std::size_t index);
    
private:
    std::uint8_t* data_;
    std::size_t data_length_;
    const bool data_owner_;
    std::size_t capacity_;
    
    std::size_t valid_start_ {0};
    std::size_t valid_end_ {0};
};

} }

#include "unsafe_fixed_circular_buffer.ipp"

