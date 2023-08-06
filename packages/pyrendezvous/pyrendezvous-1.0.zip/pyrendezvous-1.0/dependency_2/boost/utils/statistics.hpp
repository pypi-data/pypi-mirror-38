#pragma once

#include <vector>


namespace boost { namespace utils {

/**
 * @brief Methods for extraction of statistical measures from a collection of samples.
 */    
class statistics
{
public:
    statistics() = delete;
    ~statistics() = delete;
    statistics(const statistics&) = delete;
    statistics(statistics&&) = delete;
    statistics& operator=(const statistics&) = delete;
    statistics& operator=(statistics&&) = delete;
    
    /**
     * @breif Calculates a quantile of the given degree.
     * 
     * @details
     * @para
     * A quantile defined as a double in a range 0.0 - 1.0 for a sorted set of 
     * samples identifies a rate of samples which don't exceed returned sample value.
     * 
     * @para
     * Provided list of scores doesn't need to be ordered. The method will sort it 
     * itself.
     *  
     * @param scores A list of scores. 
     * @param quantile A double from a range 0-1 identifying relative devision 
     * within a number of scores.
     * @return The score value representing the requested quantile. 
     */
    template <typename T>
    static T quantile(std::vector<T> scores, double quantile);
};
    
} }

#include "statistics.ipp"
