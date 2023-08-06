#pragma once

#include <boost/memory/memory_block.hpp>

namespace boost { namespace memory {

/**
 * @brief Provides a convenient [RAII-style]
 * (https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization) mechanism
 * for owning a memory block.
 * 
 * @details
 * RAII-style binds lifespan of the allocated block with the guard object. Usage example:
 * @code
 * #include <boost/memory.hpp>
 * ...
 * using namespace boost::memory;
 * 
 * mallocator allocator;
 * allocation_guard allocation(allocator, 200ul);
 * 
 * ... 
 * @endcode 
 */
template <typename allocator_type>
class allocation_guard final
{
public:
    /**
     * @brief Allocates a block of given **size** in RAII style.
     *
     * @details
     * Using **allocator** instance, this constructor allocates memory block of the desired
     * size and binds it's lifecycle with lifecycle of this guard.
     * @param allocator The allocator instance to use.
     * @param size Desired amount of memory to allocate.
     */
    allocation_guard(allocator_type& allocator, size_t size);
    /**
     * @brief Deallocates the block.
     */
    ~allocation_guard();

    /**
     * @brief Not-copy assignable.
     */
    allocation_guard& operator=(const allocation_guard& other) = delete;

    /**
     * @brief Information about allocated underlying memory block.
     * @return Allocated memory block.
     */
    operator memory_block() const;

private:
    allocator_type& allocator_;
    memory_block allocated_block_;
};


} }

#include "allocation_guard.ipp"
