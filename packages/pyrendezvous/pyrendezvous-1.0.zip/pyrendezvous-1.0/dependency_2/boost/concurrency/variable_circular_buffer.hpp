// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "field.hpp"

#include <string>


namespace boost { namespace concurrency {

/**
 * @brief Base type for all circular buffers with variable slot length.
 */    
class variable_circular_buffer
{
public:
    variable_circular_buffer(std::string shmKey, std::size_t capacity);
    variable_circular_buffer(std::size_t capacity);
    virtual ~variable_circular_buffer();

    std::string get_shm_key() const;
    std::size_t capacity() const;
    bool empty();

protected:
    static std::size_t record_size(std::size_t size);

    std::size_t distance(std::size_t first, std::size_t second);

    const std::string shm_key_;
    const std::size_t capacity_;
    std::uint8_t* first_map_ {nullptr};
    std::uint8_t* second_map_ {nullptr};

    field<std::size_t> valid_start_;
    field<std::size_t> valid_end_;

private:
    static constexpr auto RANDOM_SHM_KEY_SIZE = 10ul;
    static constexpr auto RANDOM_ALLOWED_CHARACTERS =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    static constexpr auto FAILURE = -1;

    static std::string random_shm_key();
    static std::size_t round_page_size(std::size_t capacity);
};

} }

#include "variable_circular_buffer.ipp"

