#pragma once

#include <framework/dispatchable.hpp>

#include <functional>


namespace framework {
   
/**
 * @brief Allows execution of a function at a time in the future. 
 * 
 * @details
 * This is a base class for all timers enclosed in this framework and as such it 
 * does not implement the trigger definition. This is the responsibility of 
 * derived types.
 * 
 * There are two types of timer, one-shot timers (one_shot_timer), and 
 * auto-reload timers (auto_reload_timer). 
 * Once started, a one-shot timer will execute its callback function only once. 
 * It can be manually re-started, but will not automatically re-start itself. 
 * Conversely, once started, an auto-reload timer will automatically re-start 
 * itself after each execution of its callback function, resulting in periodic 
 * callback execution.
 * 
 * This class implements foundations shared by both of them like disarment and 
 * check of state.
 */    
class timer : public dispatchable
{
public:
    /**
     * @brief Stops the timer.
     * 
     * @details
     * Stops the timer if it's armed or does nothing if it's inactive. 
     */
    void disarm();
    /**
     * @brief Checks if the timer is started.
     * 
     * @details
     * This check determines if the timer has been armed and is expected to trigger
     * an event in the future.
     *  
     * @return **true** if the timer is started, **false** otherwise. 
     */
    bool is_armed() const;
   
protected:
    using elapsed_callback_type = std::function<void(timer&, uint64_t)>;
    
    /**
     * @brief Performs initialization of the base **timer**.
     * 
     * @param dispatcher A **dispatcher** this timer should be registered with.
     * @param elapsed_callback A callback (function, lambda expression, functor etc.)
     * which should be invoked when the scheduled time is reached.
     * @param error_callback A callback invoked in case an error is detected.
     */
    timer(
            dispatcher& dispatcher, 
            elapsed_callback_type elapsed_callback,
            error_callback_type error_callback = {});
    /**
     * @brief Forcibly disarms the timer and releases related resources.
     */
    virtual ~timer();
    
private:
    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher& dispatcher_;
    elapsed_callback_type elapsed_callback_;
};
    
}

#include "timer.ipp"