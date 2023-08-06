#pragma once

#include <iostream>
#include <string>
#include <vector>

namespace framework {

/**
 * @brief Produces a backtrace of the point where it's created.
 *
 * @details
 * An instance of this object preserves backtrace of invocation on which the
 * object has been created. An std::ostream insertion operator is overloaded to
 * write back trace with iostream.
 */
class backtrace
{
public:
    /**
     * @brief Captures stack walk of current point of execution.
     */
    backtrace();
    /**
     * @brief Makes a copy of a **backtrace**.
     * @param Another **backtrace** top copy from.
     */
    backtrace(const backtrace&);
    /**
     * @brief Destroys the **backtrace**.
     */
    ~backtrace();

    /**
     * @brief Non-heap constructable.
     */
    static void *operator new     (size_t) = delete;
    /**
     * @brief Non-heap array constructable.
     */
    static void *operator new[]   (size_t) = delete;
    /**
     * @brief Non-heap constructable.
     */
    static void  operator delete  (void*)  = delete;
    /**
     * @brief Non-heap array constructable.
     */
    static void  operator delete[](void*)  = delete;

private:
    friend std::ostream& operator<<(std::ostream& os, const backtrace& bt);

    static const std::size_t BT_BUF_SIZE = 100ul;

    void* buffer_[BT_BUF_SIZE];
    std::uint64_t nptrs_;
    char** locations_{nullptr};
};

std::ostream& operator<<(std::ostream& os, const backtrace& bt);

}

#include "backtrace.ipp"

