#pragma once

#include <framework/dispatchable.hpp>
#include <framework/dispatcher.hpp>

#include <functional>
#include <signal.h>
#include <sys/signalfd.h>
#include <unistd.h>


namespace framework {

/**
 * @brief An async handler for POSIX reliable signals
 * 
 * @details
 * @para
 * Using the handler enables dispatch of signal callback among callback triggered by other dispatchables.
 * [List of POSIX signals](http://www.comptechdoc.org/os/linux/programming/linux_pgsignals.html).
 * 
 * @para
 * Usage example:
 * @code
 * #include <framework/dispatcher.hpp>
 * #include <framework/signals/signal_handler.hpp>
 * 
 * ...
 * 
 * framework::dispatcher dispatcher;
 * framework::signal_handler handler(
 *       dispatcher, 
 *       SIGUSR1, 
 *       [](auto signo)
 *       {
 *           cout << "signal " << signo << " received" << endl;
 *       },
 *       [](auto& error)
 *       {
 *           cerr << error.what() << endl;
 *       });
 * ...
 * @endcode
 */    
class signal_handler final : public dispatchable
{
public:
    using receive_callback_type = std::function<void(int)>;
    using error_callback_type = std::function<void(std::exception)>;
    
    /**
     * @brief Initializes an instance of **signal_handler**.
     * @param dispatcher A dispatcher to register this **signal_handler** with.
     * @param signo A signal number to handle.
     * @param receive_callback a callback invoked when signal is received and dispatched.
     * @param error_callback A callback used to notify about errors.
     */
    explicit signal_handler(
            dispatcher& dispatcher, 
            int signo, 
            receive_callback_type receive_callback,
            error_callback_type error_callback = {});
    /**
     * @brief **signal_handler** deinitialization.
     */
    ~signal_handler();
    
private:
    static const int new_fd = -1;
    static const int default_flags = 0x0;
    
    virtual void handle_event(
            bool should_receive, 
            bool should_send, 
            bool should_disconnect) override;
    
    dispatcher& dispatcher_;
    receive_callback_type receive_callback_;
};
    
}

#include "signal_handler.ipp"
