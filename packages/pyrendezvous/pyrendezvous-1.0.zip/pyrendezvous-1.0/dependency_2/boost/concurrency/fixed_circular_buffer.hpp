// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "field.hpp"

#include <cstddef>
#include <cstdint>

namespace boost { namespace concurrency { 

/**
 * @brief Base class for all circular buffers with fixed size elements.
 */    
template <typename Element>    
class fixed_circular_buffer
{
public:
    /**
     * @brief Creates a buffer with the given capacity.
     * 
     * @details
     * Capacity will be rounded to the closest power of 2 greater or equal to the 
     * given capacity.
     * @param capacity The capacity for the buffer.
     */
    fixed_circular_buffer(std::size_t capacity);
    /**
     * @brief Releases related resources.
     */
    virtual ~fixed_circular_buffer();
    
    /**
     * @brief Counts number of occupied elements in the buffer.
     * @return Number of consumable elements.
     */
    std::size_t count() const;
    /**
     * @brief Retrieves element at the given index.
     * @param index Index of an element in the buffer.
     * @return 
     */
    Element* operator [](std::size_t index);
    
protected:
    std::size_t capacity_;
    std::size_t capacity_mask_;
    std::uint8_t* data_;
    std::size_t data_length_;
    
    field<std::size_t> valid_start_;
    field<std::size_t> valid_end_;
    
private:
    static std::size_t round_pow_2(std::size_t capacity);
    
};

} }

#include "fixed_circular_buffer.ipp"

