#pragma once

#include <chrono>


namespace framework {
 
inline loop::loop(dispatcher& dispatcher_arg)
        :
    dispatcher_(dispatcher_arg)    
{
    
}

inline void loop::run_forever()
{
    while (true)
    {
        if (is_interrupted_)
            break;
        
        load_fence();
        dispatcher_.dispatch(std::chrono::milliseconds(100));
    }
}

inline void loop::interrupt()
{
    is_interrupted_ = true;
}

inline void loop::interrupt_on(int signo)
{
    signal_handlers_.emplace_back(
            dispatcher_,
            signo,
            [this](auto signo) { this->interrupt(); });
}
    
}

