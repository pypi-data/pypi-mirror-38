// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "variable_circular_buffer.hpp"


namespace boost { namespace concurrency {

/**
 * @brief A void mixin for **spsc_variable_circular_buffer**.
 * 
 * @details
 * Provides an empty [mixin](http://www.drdobbs.com/cpp/mixin-based-programming-in-c/184404445) 
 * for **spsc_fixed_circular_buffer**. The intention is to have it completely optimized 
 * out during release compilation, so in-depth look at the buffer won't affect performance.
 */
class spsc_variable_circular_buffer_no_mixin
{
protected:
    static const bool MIXIN_ENABLED = false;

    void after_created(
            std::size_t& valid_start,
            std::size_t& valid_end,
            std::uint8_t* data)
    { }

    void before_push(
            const std::size_t valid_start,
            const std::size_t valid_end)
    { }

    void after_push(
            const std::size_t valid_start,
            const std::size_t valid_end,
            std::uint8_t* pushed)
    { }

    void before_consume(
        const std::size_t valid_start,
        const std::size_t valid_end)
    { }
    void after_consume(
        const std::size_t valid_start,
        const std::size_t valid_end)
    { }
};

/**
 * @brief A single producer, single consumer ring buffer with variable size element.
 * 
 * @para
 * This circular buffer accepts data pushed from a single producer thread. Also allows 
 * safe consumption with a single thread. The buffer allows publication of variables 
 * size elements.
 * 
 * @para
 * Both **push** and **consume** method calls are non-blocking and lock free. The 
 * buffer preserves order in which elements are published. Due to reduced contention
 * it should be favored over **mpsc_fixed_circular_buffer** if there's a guarantee
 * there will be only one thread pushing elements into the buffer. 
 * 
 * 
 * @tparam Mixin A type used to handle internal debug events. For a shape of this type
 * look at **spsc_variable_circular_buffer_no_mixin**.
 */
template <typename Mixin=spsc_variable_circular_buffer_no_mixin>
class spsc_variable_circular_buffer : public variable_circular_buffer, public Mixin
{
public:
    /**
     * @brief Allocates an instance of **spsc_variable_circular_buffer** backed with the 
     * given shared memory resource.
     * @param shmKey 
     * @param capacity
     */
    spsc_variable_circular_buffer(std::string shmKey, std::size_t capacity);
    /**
     * @brief Creates 
     * @param capacity
     */
    spsc_variable_circular_buffer(std::size_t capacity);
    /**
     * @brief Called upon type deallocation.
     */
    virtual ~spsc_variable_circular_buffer();

    /**
     * @brief Pushes an element onto the buffer.
     * 
     * @details
     * @para
     * This is a non-blocking method. The method will return immediately with 
     * either positive or negative result depending if publication was successful 
     * or not. This method can be executed only from one thread at a time.  
     * 
     * @para
     * Publication process is divided into 3 phases:
     * * acquisition of a buffer.
     * * assignment of data to the claimed buffer (through the callback).
     * * commit of the buffer.
     * 
     * @param callback A callback used to fill the claimed buffer with data.
     * @param size Size of the buffer to publish
     * @return **true** if publication was successful, **false** otherwise.  
     */
    template <typename Callback>
    bool push(const Callback& callback, std::size_t size);

    /**
     * @brief Consumes element(s) from the buffer.
     * @details
     * @para
     * This method checks how many element are in the buffer and attempts to consume 
     * all the elements in a single method call. For each element consumed the callback
     * is invoked. This mechanism is known as a catch up with the publication allowing 
     * efficient consumption in situation when producer and consumer are imbalanced in
     * favor of the producer. 
     * 
     * @para
     * The callback is intended to return **true** (or not return at all) in case 
     * element has been correctly consumed and can be released from the buffer.
     * If false is returned **consume** method returns immediately and the buffer 
     * for which callback returned **false** will be reprocessed upon the next consumption. 
     * 
     * @param callback
     * @return **true** if there was at least one element to consume, **false** otherwise. 
     */
    template <typename Callback>
    bool consume(const Callback& callback);

private:
    using Base = variable_circular_buffer;
};

} }

#include "spsc_variable_circular_buffer.ipp"
