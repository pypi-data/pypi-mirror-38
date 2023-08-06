#pragma once

namespace framework {
    
template <typename rep, typename period>
inline auto_reload_timer::auto_reload_timer(
        dispatcher& dispatcher,
        const std::chrono::duration<rep, period>& interval,
        elapsed_callback_type elapsed_callback,
        error_callback_type error_callback)
    :
        timer(
                dispatcher, 
                [elapsed_callback](auto& source, auto expirations) 
                { 
                    elapsed_callback(
                            static_cast<auto_reload_timer&>(source), 
                            expirations); 
                },
                error_callback),
        interval_ms_(
                std::chrono::duration_cast<std::chrono::milliseconds>(interval))
{
}

inline void auto_reload_timer::arm()
{
    auto tv_sec = interval_ms_.count() / 1000;
    auto tv_nsec = (interval_ms_.count() % 1000) * 1000000;
    
    itimerspec ts;
    ts.it_interval.tv_sec = tv_sec;
    ts.it_interval.tv_nsec = tv_nsec;
    ts.it_value.tv_sec = tv_sec;
    ts.it_value.tv_nsec = tv_nsec;

    auto settime_result = ::timerfd_settime(fd(), 0, &ts, NULL);
    check_error(settime_result);
}    
    
}

