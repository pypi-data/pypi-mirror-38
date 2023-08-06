#pragma once


namespace boost { namespace utils {
    
inline std::uint64_t timestamp::tick_count()
{
    unsigned int lo,hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}    
    
} }

