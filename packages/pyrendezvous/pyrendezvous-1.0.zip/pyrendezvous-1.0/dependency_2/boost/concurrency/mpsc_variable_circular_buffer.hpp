// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "variable_circular_buffer.hpp"


namespace boost { namespace concurrency {

/**
 * @brief A void mixin for **mpsc_variable_circular_buffer**.
 * 
 * @details
 * Provides an empty [mixin](http://www.drdobbs.com/cpp/mixin-based-programming-in-c/184404445) 
 * for **spsc_fixed_circular_buffer**. The intention is to have it completely optimized 
 * out during release compilation, so in-depth look at the buffer won't affect performance.
 */
class mpsc_variable_circular_buffer_no_mixin
{
protected:
    static const bool MIXIN_ENABLED = false;

    void after_created(
            std::size_t& valid_start,
            std::size_t& valid_end,
            std::size_t& claimed_end,
            std::uint8_t* data)
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
 * @brief Multiple producer, single consumer circular buffer with variable size element. 
 * 
* @details
 * @para
 * This circular buffer accepts data pushed from multiple producing threads, however 
 * provides means for consumption with only one thread. Each slot may have different 
 * size claimed during push.
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
 * thread producer1([&buffer]()
 * {
 *      for (uint64_t i = 0; i < LARGE_SAMPLE_COUNT; i++)
 *      {
 *          char src[i];
 *          fill_random(src, i);
 * 
 *          while (!buffer.push([&src, i](uint8_t* dst)
 *          {
 *              std::memcpy(dst, src, i);
 *          }, i));
 *      }
 *  });
 *
 *  thread producer2([&buffer]()
 *  {
 *      for (uint64_t i = 0; i < LARGE_SAMPLE_COUNT; i++)
 *      {
 *          char src[i];
 *          fill_random(src, i);
 * 
 *          while (!buffer.push([&src, i](uint8_t* dst)
 *          {
 *              std::memcpy(dst, src, i);
 *          }, i));
 *      }
 *   });
 *
 *   [...]
 *
 *   thread consumer([&buffer, &end]()
 *   {
 *       while (true)
 *       {
 *           buffer.consume([](const uint8_t* data, size_t length)
 *           {
 *               cout << length << endl;
 *               return true;
 *           });
 *       }
 *   });
 * 
 *  [...]
 * @endcode
 */
template <typename Mixin=mpsc_variable_circular_buffer_no_mixin>
class mpsc_variable_circular_buffer : public variable_circular_buffer, public Mixin
{
public:
    /**
     * @brief Allocates an **mpsc_variable_circular_buffer** using particular shared 
     * memory resource.
     * 
     * @details
     * This constructor uses either existing shared memory descriptor or allocates 
     * a new one if one doesn't exist in the system. Capacity is always rounded up 
     * to multiplication of system memory page size.
     * 
     * @param shmKey A shared memory key.
     * @param capacity Desired capacity of the buffer.
     */
    mpsc_variable_circular_buffer(std::string shmKey, std::size_t capacity);
    /**
     * @brief Allocates a **mpsc_variable_circular_buffer** using anonymous shared memory
     * resource.
     * 
     * @details
     * This constructor backs the buffer with a new shared memory resource owned 
     * by this buffer. Desired capacity is always rounded up to the closes multiplication 
     * of system memory page size.   
     * @param capacity Desired capacity for the newly created buffer.
     */
    mpsc_variable_circular_buffer(std::size_t capacity);
    /**
     * @brief Deallocates the buffer.
     */
    virtual ~mpsc_variable_circular_buffer();

    /**
     * @brief Pushes a new buffer onto the ring.
     * 
     * @details
     * This method claims a free buffer from the ring, provides it to the client 
     * through the callback and commits publication after the buffer is filled.
     * This method can be executed safely by multiple threads, tho its 
     * entry and release times maybe affected by the speed of publication from other 
     * threads - only fully filled slots can be committed and commit has to happen in 
     * the correct order.  
     * @param callback A callback invoked after a buffer from the ring is secured.
     * It should be used by the client code to copy necessary information into the buffer.
     * @return **true** if publication was successful, **false** if there are no free 
     * space to claim from the ring.  
     */
    template <typename Callback>
    bool push(const Callback& callback, std::size_t size);

    /**
     * @brief Consumes a range of buffers from the ring.
     *
     * @details 
     * @para
     * This method attempts to consume all remaining buffers from the ring. It's 
     * known as a catch up process. Through a single call to **consume** the 
     * **callback** can deliver as many buffers from the ring as there were when the method 
     * was called. Invocation of this method does not disrupt publication. 
     * 
     * @para 
     * Client code can decide if a buffer can be processed at the time. If it 
     * has been processed successfully and the ring should proceed to the next 
     * available buffer, callback should return true (or shouldn't return at all). 
     * False should be returned by the callback to indicate the current element 
     * can't be consumed at the time. Upon false result the **consume** method 
     * returns immediately and the element is available for consumption on the 
     * next **consume** method call.
     * 
     * @param callback
     * @return **true** if there was at least one buffer to consume, false otherwise.
     * It indicates only if there were buffers to consume, doesn't say anything 
     * about success or failure of consumption. 
     */
    template <typename Callback>
    bool consume(const Callback& callback);

private:
    using Base = variable_circular_buffer;

    field<std::size_t> claimed_end_;
};

} }

#include "mpsc_variable_circular_buffer.ipp"
