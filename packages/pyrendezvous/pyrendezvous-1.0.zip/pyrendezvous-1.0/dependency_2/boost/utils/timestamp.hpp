#pragma once


namespace boost { namespace utils {

/**
 * @brief A utility for reading timestamp counter off the CPU.
 * 
 * @details
 * This is a non instantiable utility providing a method emitting access to 
 * [RTDSC](http://x86.renejeschke.de/html/file_module_x86_id_278.html) instruction.
 * 
 * @link http://x86.renejeschke.de/html/file_module_x86_id_278.html
 * @link http://blog.regehr.org/archives/794
 */    
class timestamp
{
public:
    timestamp() = delete;
    ~timestamp() = delete;
    timestamp(const timestamp&) = delete;
    timestamp(timestamp&&) = delete;
    timestamp& operator=(const timestamp&) = delete;
    timestamp& operator=(timestamp&&) = delete;
    
    /**
     * @brief Reads a number of ticks elapsed.
     * 
     * @details
     * @para
     * As the time of the tick 1 isn't defined it's essential to consider the tick count
     * in a differential sense. A difference between two ticks defines number of 
     * processor cycles elapsed between two measurements.
     *  
     * @para
     * Cost of reading timestamp counter is fixed on most platforms. It's a good practice to
     * initiate performance analysis of warmed up code with measurement of time
     * required to read the counter. 
     * 
     * @return Number of cycles from CPU's timestamp counter.
     */
    static std::uint64_t tick_count();
    
};
    
} }

#include "timestamp.ipp"

