#pragma once

#include <cstddef>
#include <cstdint>


namespace boost { namespace concurrency {
    
/**
 * @brief Full memory barried.
 */
inline void thread_fence()
{
    asm volatile("" ::: "memory");
}

/**
 * @brief Load memory barrier.
 */
inline void load_fence()
{
    asm volatile("lfence");
}

/**
* @brief Fence operation that uses locked addl as mfence is sometimes expensive
*/
inline void fence()
{
    asm volatile("lock; addl $0,0(%%rsp)" : : : "cc", "memory");
}

inline void acquire()
{
    volatile std::int64_t* dummy;
    asm volatile("movq 0(%%rsp), %0" : "=r" (dummy) : : "memory");
}

inline void release()
{
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-variable"
    // Avoid hitting the same cache-line from different threads.
    volatile std::int64_t dummy = 0;
}
// must come after closing brace so that gcc knows it is actually unused
#pragma GCC diagnostic pop

/**
* @brief A more jitter friendly alternate to thread:yield in spin waits.
*/
inline void cpu_pause()
{
    asm volatile("pause\n": : :"memory");
}

/**
 * @brief Returns a 64 bit integer with volatile semantics.
 * 
 * @details
 * On x64 MOV is a SC Atomic a operation.
 */
inline std::size_t get_int64_volatile(volatile std::size_t* source)
{
    size_t sequence = *reinterpret_cast<volatile std::size_t *>(source);
    thread_fence();
    return sequence;
}

/**
 * @brief Put a 64 bit int with volatile semantics.
 */
inline void put_int64_volatile(volatile std::size_t*  address, std::size_t value)
{
    thread_fence();
    *reinterpret_cast<volatile std::size_t *>(address) = value;
}

/**
 * @brief Put a 64 bit int with atomic semantics.
 **/
inline void put_int64_atomic(volatile std::size_t*  address, std::size_t value)
{
    asm volatile(
        "xchgq (%2), %0"
        : "=r" (value)
        : "0" (value), "r" (address)
        : "memory");
}

/**
 * @brief Compare and exchange (CAS).
 * 
 * @details
 * Atomically compares the destination with the expected value, if they match 
 * destination is replaced with desired value. The operation returns initial value
 * of the destination.
 * 
 * @param destination Destination address to store the result.
 * @param expected Expected value in the destination.
 * @param desired Value to change the destination to. 
 * @return Original value of the destination.
 */
inline std::size_t cmpxchg(volatile std::size_t* destination, std::size_t expected, std::size_t desired)
{
    std::size_t original;
    asm volatile(
                 "lock; cmpxchgq %2, %1"
                 : "=a"(original), "+m"(*destination)
                 : "q"(desired), "0"(expected));
    return original;
}
    
} }

