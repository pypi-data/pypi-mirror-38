#pragma once

#include <cerrno>
#include <cstring>
#include <sstream>


namespace framework {

template <typename error_type>
inline error_handler<error_type>::error_handler(
        error_callback_type error_callback)
    :
        error_callback_(error_callback)
{
    
}

template <typename error_type>
template <error_level level>
inline void error_handler<error_type>::raise_error(int error_code) const
{
    if (error_callback_)
    {
        std::stringstream ss;
        ss << "error(" << errno << ") " << strerror(errno);

        error_type error(error_code, ss.str());
        error_callback_(error);

        if (level == error_level::lethal)
            throw error;
    }
    else if (level == error_level::lethal)
    {
        std::stringstream ss;
        ss << "error(" << errno << ") " << strerror(errno);
        throw error_type(error_code, ss.str());
    }
}
    
template <typename error_type>
template <typename result_type, error_level level>
inline bool error_handler<error_type>::check_error(result_type result) const
{
    if (result == result_error)
    {
        if (errno == EAGAIN)
            return false;
        
        if (errno == EINPROGRESS)
            return true;
        
        raise_error<level>(errno);
    }
    
    return true;
}

template <typename error_type>
template <typename result_type>
inline bool error_handler<error_type>::check_lethal_error(result_type result) const
{
    return check_error<result_type, error_level::lethal>(result);
}
    
}
