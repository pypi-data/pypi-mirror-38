#pragma once

#include "statistics.hpp"

#include <algorithm>


namespace boost { namespace utils {

template <typename T>
inline T statistics::quantile(std::vector<T> scores, double quantile)
{
    std::sort(scores.begin(), scores.end());

    std::size_t size = scores.size();
    std::size_t rank = static_cast<double>(size) * quantile;
    return scores[rank];
}
    
} }
