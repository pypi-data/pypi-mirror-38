#pragma once

#include <unistd.h>


namespace framework {
   
inline int dispatchable::fd() const
{
    return fd_;
}    
    
inline dispatchable::dispatchable(
        error_callback_type error_callback)
    :
        rendezvous_error_handler(error_callback)
{  
}

inline dispatchable::~dispatchable()
{
    if (fd_ != no_fd)
        ::close(fd_);
}

inline void dispatchable::set_fd(int fd)
{
    fd_ = fd;
}
    
}
