#pragma once 

#include <bitset>


namespace boost { namespace concurrency {
    
namespace current_thread {
    
static const auto RESULT_OK = 0;    

using affinity_mask = std::bitset<128>;

affinity_mask operator"" _mask (const char* str);

/**
 * @brief Pins current thread to physical cores according to the provided *mask*.
 * 
 * @param mask A [bitset](http://www.cplusplus.com/reference/bitset/bitset/) inidicating 
 * which cores should be used to service current thread.
 */
void set_affinity(affinity_mask mask);
    
}
    
} }

#include "current_thread.ipp"

