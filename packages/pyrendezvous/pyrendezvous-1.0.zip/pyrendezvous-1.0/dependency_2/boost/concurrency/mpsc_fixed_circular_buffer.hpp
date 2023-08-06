// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "field.hpp"
#include "fixed_circular_buffer.hpp"

#include <cstddef>
#include <cstdint>


namespace boost { namespace concurrency {

/**
 * @brief A void mixin for **mpsc_fixed_circular_buffer**.
 * 
 * @details
 * Provides an empty [mixin](http://www.drdobbs.com/cpp/mixin-based-programming-in-c/184404445) 
 * for **mpsc_fixed_circular_buffer**. The intention is to have it completely optimized 
 * out during release compilation, so in-depth look at the buffer won't affect performance.  
 */    
class mpsc_fixed_circular_buffer_no_mixin
{
protected:
    static const bool MIXIN_ENABLED = false;

    void after_created(
            std::size_t& valid_start,
            std::size_t& valid_end,
            std::size_t& claimed_end)
    { }

    void before_push(
            const size_t valid_start,
            const size_t valid_end,
            const size_t claimed_end)
    { }

    void after_claim(
            const std::size_t valid_start,
            const std::size_t valid_end,
            const std::size_t claimed_end)
    { }

    void failed_commit(
            std::size_t valid_start,
            std::size_t valid_end,
            std::size_t claimed_end)
    { }

    void after_commit(
            const std::size_t valid_start,
            const std::size_t valid_end,
            const std::size_t claimed_end)
    { }

    void after_push(
            const std::size_t valid_start,
            const std::size_t valid_end,
            const std::size_t claimed_end)
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
 * @brief Multiple producers, single consumer circular buffer with fixed size elements.
 * 
 * @details
 * @para
 * This circular buffer accepts data pushed from multiple producing threads, however 
 * provides means for consumption with only one thread. All slots have equal size.
 * Each capable to accommodate a single instance of type **Element**.
 * 
 * @para
 * Both **push** and **consume** method calls are non-blocking and lock free. The 
 * buffer preserves order in which elements are published. Thus parallel publications
 * have to wait with slot commit until all previously claimed slots are submitted. 
 * 
 * @para
 * Usage example:
 * @code
 * #include <boost/concurrency.hpp>
 *
 * [...]
 * thread producer1([&buffer, &start1]()
 * {
 *      for (uint64_t i = 0; i < LARGE_SAMPLE_COUNT; i++)
 *      {
 *          while (!buffer.push([i](Element& element)
 *          {
 *              timespec time;
 *              clock_gettime(CLOCK_REALTIME, &time);
 *
 *              element.producer = 1;
 *              element.time = time;
 *          }));
 *      }
 *  });
 *
 *  thread producer2([&buffer, &start2]()
 *  {
 *      for (auto i = 0ul; i < LARGE_SAMPLE_COUNT; i++)
 *      {
 *          while (!buffer.push([i](Element& element)
 *          {
 *              timespec time;
 *              clock_gettime(CLOCK_REALTIME, &time);
 *
 *               element.producer = 2;
 *               element.time = time;
 *           }));
 *       }
 *   });
 *
 *   [...]
 *
 *   thread consumer([&buffer, &end]()
 *   {
 *       while (true)
 *       {
 *           buffer.consume([](const Element& element)
 *           {
 *               cout << element.producer << " : " << element.time << endl;
 *               return true;
 *           });
 *       }
 *   });
 * 
 *  [...]
 * @endcode 
 */
template <typename Element, typename Mixin=mpsc_fixed_circular_buffer_no_mixin>
class mpsc_fixed_circular_buffer 
        : public fixed_circular_buffer<Element>, public Mixin
{
public:
    /**
     * @brief Allocates a **mpsc_fixed_circular_buffer** with the given capacity.
     * 
     * @details
     * The underlying ring buffer capacity is rounded to the closest power of 2 
     * greater or equal to the given capacity.   
     * @param capacity Desired number of slots in the buffer.
     */
    mpsc_fixed_circular_buffer(std::size_t capacity);
    /**
     * @brief Deallocates the buffer.
     */
    virtual ~mpsc_fixed_circular_buffer();

    /**
     * @brief Pushes an element onto the buffer.
     * 
     * @details
     * This method claims a free element of the buffer, provides it to the client 
     * code through the callback and commits publication after the element is filled
     * with data. This method can be executed safely by multiple threads, tho its 
     * enter and exit times maybe affected by the speed of publication from other 
     * threads - only fully filled slots can be committed and commit has to happen in 
     * the correct order.  
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
     * known as a catch up process, where through a single call to **consume** the 
     * **callback** can deliver as many elements from the buffer as there were when the method 
     * was invoked. Invocation of this method does not disrupt publication. 
     * 
     * @para 
     * Client code can decide if an element can be processed at the time. If it 
     * has been processed successfully and the buffer should proceed to the next 
     * available element callback should return true. False returned by the callback indicates
     * the current element can;t be consumed at the time. Thus the **consume** 
     * method returns immediately and the element is available for consumption again
     * upon **consume** method call. 
     * @param callback
     * @return **true** if there was at least one element to consume, false otherwise.
     * It indicates only if there were elements to consume, doesn't say anything 
     * about success or failure of consumption. 
     */
    template <typename Callback>
    bool consume(const Callback& callback);

private:
    using Base = fixed_circular_buffer<Element>;
    
    field<std::size_t> claimed_end_;
};

} }

#include "mpsc_fixed_circular_buffer.ipp"

