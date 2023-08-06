#pragma once

#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>
#include <framework/timers/timer.hpp>

#include <chrono>
#include <functional>


namespace framework {
  
/**
 * @brief Repeatedly raises an event on given intervals.
 * 
 * @details
 * @para
 * Auto reload timer automatically re-starts itself after each execution of its 
 * callback function.
 * 
 * @para
 * A newly created **auto_reload_timer** is disarmed. Callback function is invoked at 
 * regular intervals after **arm** method is called. 
 */    
class auto_reload_timer final : public timer
{
public:
    using elapsed_callback_type = std::function<void(auto_reload_timer&, uint64_t)>;
    
    /**
     * @brief Creates an instance of **auto_reload_timer**.
     * 
     * @param dispatcher A dispatcher this timer will be registered with.
     * @param interval An interval at which 
     * @param elapsed_callback
     * @param error_callback
     */
    template <typename rep, typename period>
    explicit auto_reload_timer(
            dispatcher& dispatcher,
            const std::chrono::duration<rep, period>& interval,
            elapsed_callback_type elapsed_callback,
            error_callback_type error_callback = {});
    
    /**
     * @brief Starts the timer.
     * 
     * @details
     * Once started the timer will invoke the callback registered in the constructor
     * on equal intervals. If timer is delayed due to over congested use of dispatchers
     * queue a number of expirations covered by the event is stated in the callback.
     */
    void arm();
    
private:
    const std::chrono::milliseconds interval_ms_;
};

/**
 * @example framework/timers/auto_reload_timer.cpp
 * 
 * An example showing how to initialize and use **auto_reload_timer**.
 */
    
}

#include "auto_reload_timer.ipp"

