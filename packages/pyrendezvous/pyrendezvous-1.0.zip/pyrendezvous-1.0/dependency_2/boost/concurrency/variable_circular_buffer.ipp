// Copyright (c) 2016 Lukasz Laszko
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#pragma once

#include "variable_circular_buffer.hpp"

#include <cerrno>
#include <cstring>
#include <sstream>
#include <stdexcept>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


namespace boost { namespace concurrency {

inline variable_circular_buffer::variable_circular_buffer(std::string shmKey, std::size_t capacity)
        :
    shm_key_(shmKey),
    capacity_(round_page_size(capacity))
{
    auto fd = ::shm_open(shm_key_.c_str(), O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
    if (fd == FAILURE)
    {
        std::stringstream ss;
        ss << "shm_open: error(" << errno << ") " << ::strerror(errno);
        throw std::invalid_argument(ss.str());
    }

    auto result = ::ftruncate(fd, capacity_);
    if (result == FAILURE)
    {
        std::stringstream ss;
        ss << "ftruncate: error(" << errno << ") " << ::strerror(errno);
        throw std::invalid_argument(ss.str());
    }

    // first mapping uses 2 * capacity to establish space also for the second mapping
    // as use of MAP_FIXED requires use of address which is valid. Otherwise on rare occasions
    // second mapping could be established in boundries which aren't valid
    auto map = ::mmap(NULL, 2ul * capacity_, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED)
    {
        std::stringstream ss;
        ss << "mmap: error(" << errno << ") " << ::strerror(errno);
        throw std::invalid_argument(ss.str());
    }

    first_map_ = reinterpret_cast<uint8_t*>(map);

    auto expected_second_map = first_map_ + capacity_;
    map = ::mmap(expected_second_map, capacity_, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_FIXED, fd, 0);
    if (map == MAP_FAILED)
    {
        std::stringstream ss;
        ss << "mmap: error(" << errno << ") " << ::strerror(errno);
        throw std::invalid_argument(ss.str());
    }
    else if (map != expected_second_map)
    {
        std::stringstream ss;
        ss << "mmap: requested mapped block 0x" << std::hex << expected_second_map << " but is 0x" << std::hex << map;
        throw std::invalid_argument(ss.str());
    }

    second_map_ = reinterpret_cast<uint8_t*>(map);
}

inline variable_circular_buffer::variable_circular_buffer(std::size_t capacity)
        :
    variable_circular_buffer(random_shm_key(), capacity)
{
}

inline variable_circular_buffer::~variable_circular_buffer()
{
    if (second_map_ != nullptr)
    {
        ::munmap(second_map_, capacity_);
        second_map_ = nullptr;
    }

    if (first_map_ != nullptr)
    {
        ::munmap(first_map_, capacity_);
        first_map_ = nullptr;
    }

    ::shm_unlink(shm_key_.c_str());
}

inline std::string variable_circular_buffer::get_shm_key() const
{
    return shm_key_;
}

inline std::size_t variable_circular_buffer::capacity() const
{
    return capacity_;
}

inline bool variable_circular_buffer::empty()
{
    return valid_start_.read_dirty() == valid_end_.read_dirty();
}

inline std::size_t variable_circular_buffer::round_page_size(std::size_t capacity)
{
    auto page_size = getpagesize();
    return capacity % page_size == 0
         ? capacity
         : (capacity / page_size + 1) * page_size;
}

inline std::string variable_circular_buffer::random_shm_key()
{
    srand(time(NULL));

    std::stringstream shm_key;
    for (auto i = 0ul; i < RANDOM_SHM_KEY_SIZE; i++)
        shm_key << RANDOM_ALLOWED_CHARACTERS[rand() % sizeof(RANDOM_ALLOWED_CHARACTERS)];

    return shm_key.str();
}

inline std::size_t variable_circular_buffer::record_size(std::size_t size)
{
    return sizeof(std::size_t) + size;
}

inline std::size_t variable_circular_buffer::distance(std::size_t first, std::size_t second)
{
    if (second > first)
        return second - first;
    else
        return capacity_ + (second - first);
}

} }

