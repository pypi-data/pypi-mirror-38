#pragma once

#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>
#include <framework/timers/timer.hpp>

#include <chrono>
#include <functional>


namespace framework {

/**
 * @brief Raises an event only once after scheduled interval.
 * 
 * @details
 * This type of timer triggers registered callback only once after scheduled time.
 *  
 */
class one_shot_timer final : public timer
{
public:
    using elapsed_callback_type = std::function<void(one_shot_timer&)>;

    /**
     * @brief Creates an instance of **one_shot_timer**.
     * 
     * @param dispatcher A **dispatcher** with which the timer should be registered.
     * @param elapsed_callback A callback invoked when timer is elapsed.
     * @param error_callback A callback invoked in event of error(s).
     */
    explicit one_shot_timer(
            dispatcher& dispatcher,
            elapsed_callback_type elapsed_callback,
            error_callback_type error_callback = {});

    /**
     * @brief Schedules event invocation after the given delay.
     *  
     * @param delay A delay after which the callback will be invoked.
     */
    template <typename rep, typename period>
    void schedule(const std::chrono::duration<rep, period>& delay);
};

/**
 * @example framework/timers/one_shot_timer.cpp
 * 
 * An example illustrating use of **one_shot_timer**.
 */

}

#include "one_shot_timer.ipp"

