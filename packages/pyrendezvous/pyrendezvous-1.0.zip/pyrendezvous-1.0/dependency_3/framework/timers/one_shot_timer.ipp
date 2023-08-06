#pragma once

#include <sys/timerfd.h>


namespace framework {

inline one_shot_timer::one_shot_timer(
        dispatcher& dispatcher,
        elapsed_callback_type elapsed_callback,
        error_callback_type error_callback)
    :
        timer(
                dispatcher, 
                [elapsed_callback](auto& source, auto expirations) 
                { 
                    elapsed_callback(static_cast<one_shot_timer&>(source)); 
                },
                error_callback)
{
}

template <typename rep, typename period>
inline void one_shot_timer::schedule(const std::chrono::duration<rep, period>& delay)
{
    auto delay_ms = std::chrono::duration_cast<std::chrono::milliseconds>(delay);

    itimerspec ts;
    ts.it_interval.tv_sec = 0;
    ts.it_interval.tv_nsec = 0;
    ts.it_value.tv_sec = delay_ms.count() / 1000;
    ts.it_value.tv_nsec = (delay_ms.count() % 1000) * 1000000;

    auto settime_result = ::timerfd_settime(fd(), 0, &ts, NULL);
    check_error(settime_result);
}

}

