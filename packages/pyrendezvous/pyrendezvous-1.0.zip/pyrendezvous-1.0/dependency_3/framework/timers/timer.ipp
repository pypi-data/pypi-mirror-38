#pragma once

#include <cerrno>
#include <sys/timerfd.h>


namespace framework {

inline void timer::disarm()
{
    itimerspec new_ts;
    itimerspec old_ts;
    new_ts.it_interval.tv_sec = 0;
    new_ts.it_interval.tv_nsec = 0;
    new_ts.it_value.tv_sec = 0;
    new_ts.it_value.tv_nsec = 0;

    auto settime_result = ::timerfd_settime(fd(), 0, &new_ts, &old_ts);
    check_error(settime_result);
}

inline bool timer::is_armed() const
{
    itimerspec ts;
    auto gettime_result = timerfd_gettime(fd(), &ts);
    check_lethal_error(gettime_result);

    return ts.it_value.tv_sec != 0ul || ts.it_value.tv_nsec != 0ul;
}

inline timer::timer(
        dispatcher& dispatcher,
        elapsed_callback_type elapsed_callback,
        error_callback_type error_callback)
    :
        dispatchable(error_callback),
        dispatcher_(dispatcher),
        elapsed_callback_(elapsed_callback)
{
    auto timerfd = ::timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK);
    check_lethal_error(timerfd);

    dispatchable::set_fd(timerfd);
    dispatcher_.add(*this, true, false, false, false);
}

inline timer::~timer()
{
    dispatcher_.remove(*this);
}

inline void timer::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    uint64_t expirations;
    auto read_result = read(fd(), &expirations, sizeof(expirations));
    if (check_error(read_result))
    {
        if (expirations > 0)
        {
            if (elapsed_callback_)
                elapsed_callback_(*this, expirations);
        }
    }
}

}