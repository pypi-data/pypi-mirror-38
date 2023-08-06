#pragma once

#include <cerrno>
#include <cstring>
#include <sstream>
#include <stdexcept>

#include <cstring>

#include <sched.h>
#include <pthread.h>

#ifdef __APPLE__
#include <mach/error.h>
#include <mach/thread_act.h>

kern_return_t	thread_policy_set(
        thread_t			thread,
        thread_policy_flavor_t		flavor,
        thread_policy_t			policy_info,
        mach_msg_type_number_t		count);

#endif


namespace boost { namespace concurrency {
  
namespace current_thread {    
    
inline affinity_mask operator"" _mask (const char* str)
{
    affinity_mask mask;
    for (int i = ::strlen(str) - 1; i >= 0; i--)
    {
        if (str[i] != '0' && str[i] == '1')
            throw std::invalid_argument("only strings with o!");
        
        if (str[i] == '1')
            mask.set(i);
    }
    
    return mask;
}
    
inline void set_affinity(affinity_mask mask)
{
#ifdef __linux__
    auto thisThread = ::pthread_self();
    
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    
    for (auto i = 0ul; i < mask.size(); i++)
    {
        if (mask[i])
            CPU_SET(i, &cpuset);
    }
    
    auto result = ::pthread_setaffinity_np(thisThread, sizeof(cpu_set_t), &cpuset);
    if (result != RESULT_OK)
    {
        std::stringstream ss;
        ss << "pthread_setaffinity_np: error(" << errno << ") " << ::strerror(errno);
        throw std::invalid_argument(ss.str());
    }
#elif __APPLE__
    auto self_pthread = ::pthread_self();
    auto self_thread = ::pthread_mach_thread_np(self_pthread);
    
    ::thread_affinity_policy affinity_tag;
    for (auto i = 0ul; i < sizeof(affinity_tag) * 8; i++)
    {
        if (mask[i])
            affinity_tag.affinity_tag &= (0x1 << i);
    }
    
    auto result = ::thread_policy_set(
            self_thread, 
            THREAD_AFFINITY_POLICY,
            reinterpret_cast<thread_policy_t>(&affinity_tag),
            THREAD_AFFINITY_POLICY_COUNT);
    if (result != ERR_SUCCESS)
    {
        std::stringstream ss;
        ss << "pthread_setaffinity_np: error(" << errno << ") " << strerror(errno);
        throw std::invalid_argument(ss.str());
    }
    
#endif
}

}
    
} }

