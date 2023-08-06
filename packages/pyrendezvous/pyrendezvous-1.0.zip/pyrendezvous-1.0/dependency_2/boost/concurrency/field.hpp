// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "atomic.hpp"

#include <cstdint>
#include <type_traits>


namespace boost { namespace concurrency {

#if defined(__aarch64__)
#define CACHE_LINE_SIZE 64
#elif defined(__arm__)
#define CACHE_LINE_SIZE 32
#elif defined(__amd64__)
#define CACHE_LINE_SIZE 64
#else
#   error Unsupported CPU architecture
#endif

/**
 * @brief Represents a cache line exclusive field. The field is stretched to size of 2 cache lines.
 * 
 * The smallest unit portion of memory recognized by cache coherency mechanism is 
 * cache line. It means fetch, store, lock related to a memory cell in fact relates 
 * not only to that cell but also other cells within the same cache line. In order to 
 * ensure that operations on the field don;t affect other cache lines this type provides 'safe'
 * reserved surrounding for that field. Additionally, a range of operations with and 
 * without memory fencing, locking have been provided.       
 */
template <typename field_type> 
class alignas(2 * CACHE_LINE_SIZE) field
{
public:
    static_assert(
            std::is_same<field_type, std::size_t>::value
            || std::is_same<field_type, std::int32_t>::value
            || std::is_same<field_type, std::uint32_t>::value
            || std::is_same<field_type, std::int64_t>::value
            || std::is_same<field_type, std::uint64_t>::value,
            "Unsupported field type");
    
    /**
     * @brief Reads the field value directly without imposing any memory barrier.
     * @return Field value.
     */
    inline field_type read_dirty() const
    {
        return sequence_;
    }

    /**
     * @brief Reads the field and imposes a read memory barrier after this read.
     * 
     * Imposing a load memory barrier after reading a field notifies hardware that
     * all load operations before the barrier should be finialised before crossing 
     * the barrier.  
     * 
     * @return Field value.
     */
    inline field_type read_fenced() const
    {
        auto value = sequence_;
        load_fence();
        
        return value;
    }

    /**
     * @brief Performs a volatile read of the underlying field.
     * 
     * A volatile read imposes a full memory barrier after the read. It means all
     * read and write operations should be finalized by the hardware before the barrier is crossed.
     * No store/load instructions can be reordered across the barrier. 
     * 
     * @return Field value
     */
    field_type read_volatile()
    {
        return get_int64_volatile(reinterpret_cast<volatile std::size_t*>(&sequence_));
    }

    /**
     * @brief Imposes a full memory barrier and set value to the underlying field.
     * 
     * Full memory barrier imposed before store operation guarantees that all stores and 
     * loads issued before this method will be finalized before the value is store in
     * the underlying field.
     * 
     * @param value Value to set
     */
    void put_fenced(field_type value)
    {
        thread_fence();
        sequence_ = value;
    }

    /**
     * @brief Compares the current field value with *expected*, if they are equal
     * the field is set with the *value*.
     * 
     * It is a CAS operation which performs a cache line lock and atomically updates 
     * underlying field value if the condition is met. 
     * 
     * @param expected The expected value of the field which will trigger update.
     * @param value The value to set the field to if the condition is met.
     * @return True on success, False on failure.
     */
    bool compare_exchange(field_type expected, field_type value)
    {
        return cmpxchg(
                reinterpret_cast<volatile field_type*>(&sequence_),
                expected,
                value) == expected;
    }

private:
    std::uint8_t reserved_[CACHE_LINE_SIZE - sizeof(field_type)];
    field_type sequence_{0};
};

} }

