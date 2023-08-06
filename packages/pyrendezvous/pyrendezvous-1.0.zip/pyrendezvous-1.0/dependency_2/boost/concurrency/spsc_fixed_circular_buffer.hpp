// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "fixed_circular_buffer.hpp"

#include <cstddef>
#include <cstdint>


namespace boost { namespace concurrency {

/**
 * @brief A void mixin for **spsc_fixed_circular_buffer**.
 * 
 * @details
 * Provides an empty [mixin](http://www.drdobbs.com/cpp/mixin-based-programming-in-c/184404445) 
 * for **spsc_fixed_circular_buffer**. The intention is to have it completely optimized 
 * out during release compilation, so in-depth look at the buffer won't affect performance.  
 */     
class spsc_fixed_circular_buffer_no_mixin
{
protected:
    static const bool MIXIN_ENABLED = false;

    void after_created(
            std::size_t& validStart,
            std::size_t& validEnd)
    { }

    void before_push(
            const std::size_t validStart,
            const std::size_t validEnd)
    { }

    template <typename Element>
    void after_push(
            const std::size_t validStart,
            const std::size_t validEnd,
            Element* pushed)
    { }

    void before_consume(
        const std::size_t validStart,
        const std::size_t validEnd)
    { }
    void after_consume(
        const std::size_t validStart,
        const std::size_t validEnd)
    { }
};

/**
 * @brief Single producer, single consumer circular buffer with fixed size elements.
 * 
 * @details
 * @para
 * This circular buffer accepts data pushed from a single producer thread. Also allows 
 * safe consumption from only one thread. All slots have equal sizes. Each capable to 
 * accommodate a single instance of type **Element**.
 * 
 * @para
 * Both **push** and **consume** method calls are non-blocking and lock free. The 
 * buffer preserves order in which elements are published. Due to reduced contention
 * it should be favored over **mpsc_fixed_circular_buffer** if there's a guarantee
 * there will be only one thread pushing elements into the buffer. 
 * 
 * @para
 * Usage example:
 * @code
 *  #include <boost/concurrency.hpp>
 *
 *  [...]
 *  // producer
 *  thread producer([&buffer, &start]()
 *  {
 *      start = timestamp::tick_count();
 *      for (uint64_t i = 0; i < LARGE_SAMPLE_COUNT; i++)
 *      {
 *          while (!buffer.push([i](Element& element)
 *          {
 *              element.id = i;
 *          }));
 *      }
 *  });
 *
 *  [...]
 *
 *  // consumer
 *  thread consumer([&buffer, &end]()
 *  {
 *      uint64_t count = 0;
 *      while (count < LARGE_SAMPLE_COUNT)
 *      {
 *          buffer.consume([&count, &buffer](const Element& element)
 *          {
 *              if (element.id != count++)
 *                  throw "element.id != count++";
 * 
 *              return true;
 *          });
 *      }
 *      end = timestamp::tick_count();
 *  });
 * 
 *  [...]
 * @endcode 
 */
template <typename Element, typename Mixin=spsc_fixed_circular_buffer_no_mixin>
class spsc_fixed_circular_buffer : public fixed_circular_buffer<Element>, public Mixin
{
public:
    /**
     * @brief Allocates a **spsc_fixed_circular_buffer** with the given capacity.
     * 
     * @details
     * The underlying ring buffer capacity is rounded to the closest power of 2 
     * greater or equal to the given capacity.   
     * @param capacity Desired number of slots in the buffer.
     */
    spsc_fixed_circular_buffer(std::size_t capacity);
    /**
     * @brief Deallocates the buffer.
     */
    virtual ~spsc_fixed_circular_buffer();

    /**
     * @brief Pushes an element onto the buffer.
     * 
     * @details
     * This method claims a free element of the buffer, provides it to the client 
     * through the callback and commits publication after the element is filled
     * with data. This method can be executed safely only from one thread at a time.
     * @param callback A callback invoked after an element from the buffer is secured,
     * should be used by the client code to copy necessary information into the element.
     * @return **true** if publication was successful, **false** if there are no free 
     * elements to claim from the buffer.  
     */
    template <typename Callback>
    bool push(const Callback& callback);

    /**
     * @brief Consumes an element from the buffer.
     * 
     * @details
     * @para
     * This method attempts to consume all remaining elements from the buffer. It's 
     * known as a catch up process. During a single call to **consume** the 
     * **callback** can deliver as many elements from the buffer as there were elements 
     * when the method was invoked. Invocation of this method does not disrupt publication. 
     * 
     * @para 
     * Client code can decide if an element can be processed at the time. If it 
     * has been processed successfully and the buffer should proceed to the next 
     * available element callback should return true (or shouldn't return at all). 
     * False result indicates an error during consumption and retry on the next consumption. 
     * Thus the **consume** method returns immediately and the element is available for
     * consumption upon the next **consume** method call. 
     * @param callback
     * @return **true** if there was at least one element to consume, false otherwise.
     * It indicates only if there were elements to consume, doesn't say anything 
     * about success or failure of consumption. 
     */
    template <typename Callback>
    bool consume(const Callback& callback);

private:
    using Base = fixed_circular_buffer<Element>;
    
};

} }

#include "spsc_fixed_circular_buffer.ipp"

