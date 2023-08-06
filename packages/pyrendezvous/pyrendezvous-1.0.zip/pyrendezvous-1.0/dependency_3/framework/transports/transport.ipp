#pragma once

#include <framework/errors/rendezvous_error.hpp>


namespace framework {

inline transport::transport(error_callback_type error_callback)
        :
    dispatchable(error_callback)
{

}

inline transport::~transport()
{

}

inline void transport::throw_on_wrong_fd()
{
    if (fd() == no_fd)
        throw rendezvous_error(0, "underlying file descriptor is not set!");
}

}
