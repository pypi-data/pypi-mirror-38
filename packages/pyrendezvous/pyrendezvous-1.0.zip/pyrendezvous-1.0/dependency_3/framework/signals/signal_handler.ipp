#pragma once

#include <cerrno>
#include <cstring>
#include <sstream>
#include <stdexcept>

#include "signal_handler.hpp"


namespace framework {

inline signal_handler::signal_handler(
        dispatcher& dispatcher,
        int signo,
        receive_callback_type receive_callback,
        error_callback_type error_callback)
    :
        dispatchable(error_callback),
        dispatcher_(dispatcher),
        receive_callback_(receive_callback)
{
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, signo);

    auto procmask_result = sigprocmask(SIG_BLOCK, &mask, NULL);
    check_lethal_error(procmask_result);

    auto fd_result = signalfd(new_fd, &mask, default_flags);
    check_lethal_error(fd_result);

    dispatchable::set_fd(fd_result);
    dispatcher_.add(*this, true, false, false, false);
}

inline signal_handler::~signal_handler()
{
    dispatcher_.remove(*this);
}

inline void signal_handler::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    signalfd_siginfo si;
    auto read_result = read(fd(), &si, sizeof(si));
    if (check_lethal_error(read_result))
    {
        if (size_t(read_result) < sizeof(si))
        {
            throw std::logic_error("Invalid number of bytes received from signalfd!");
        }

        if (receive_callback_)
            receive_callback_(si.ssi_signo);
    }
}

}
