#pragma once

#include <framework/dispatcher.hpp>
#include <framework/signals/signal_handler.hpp>

#include <list>


namespace framework {

/**
 * @brief Dispatch loop for a dispatcher.
 * 
 * @details
 * It is a central execution device provided by the framework. Provides a declarative
 * interface for interruptable dispatch loop on referenced **dispatcher**. 
 */
class loop
{
public:
    /**
     * @brief Creates a loop over the given **dispatcher**.
     * @param dispatcher_arg A dispatcher the loop will operate over.
     */
    explicit loop(dispatcher& dispatcher_arg);
    
    /**
     * @brief A loop invoking **dispatch** on the underlying **dispatcher**.
     * @details
     * The loop runs indefinitely unless **interrupt** is called or any of signals
     * registered with **interrupt_on** is raised.
     */ 
    void run_forever();
    
    /**
     * @brief Interrupts **run_forever**.
     */
    void interrupt();
    
    /**
     * @brief Triggers **interrupt** on the given signal.
     * 
     * @param signo A valid system signal number.
     */
    void interrupt_on(int signo);
    
private:
    inline void load_fence()
    {
        asm volatile("lfence");
    }
    
    dispatcher& dispatcher_;
    bool is_interrupted_{false};
    
    std::list<signal_handler> signal_handlers_;
};
    
}

#include "loop.ipp"

