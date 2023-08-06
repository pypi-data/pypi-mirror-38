#pragma once

#include <framework/dispatchable.hpp>

#include <chrono>
#include <stdexcept>
#include <sys/epoll.h>
#include <unordered_set>


namespace framework {

/**
 * @brief Dispatches events from a I/O queue to dispatchables.
 *
 * @details
 * A dispatcher design pattern allows a **dispatchable** to register itself with
 * and receive notifications from a provider whenever there's a need to undertake
 * an operation in the related I/O queue for a file descriptor the **dispatchable**
 * is related to.
 *
 * Dispatcher manages underlying I/O queue, peeks up events during a **dispatch**
 * call. If there are any new events in that queue it notifies **dispatchable**
 * about actions requested from it by that event.
 *
 * **dispatcher**s can be organized in a hierarchy, where underlying queue can be
 * registered as an event source for higher level dispatchers. In such case parent
 * dispatchers can be used to dispatch events for dispatchables  managed by it's children.
 *
 * There's a strong relation between **dispatcher** and **dispatchable**. A **dispatchable**
 * can be managed only by a single **dispatcher**.
 */
class dispatcher final : public dispatchable
{
public:
    using milliseconds = std::chrono::milliseconds;

    static const int default_max_events = 64;

    /**
     * @brief Creates a root level **dispatcher**
     *
     * @details
     * This constructor creates a root level dispatcher, events for the underlying
     * I/O queue can be dispatched only by this dispatcher.
     *
     * @param error_callback An error handler for dispatcher errors.
     */
    dispatcher(error_callback_type error_callback = {});
    /**
     * @brief Creates a dependent **dispatcher**
     *
     * @details
     * Events from a dependent dispatcher can be dispatched by either this dispatcher
     * or any of it's parents.
     * @param parent Parent dispatcher.
     * @param error_callback An error handler for dispatcher errors.
     */
    dispatcher(
            dispatcher& parent,
            error_callback_type error_callback = {});
    /**
     * @brief Called upon destruction.
     */
    virtual ~dispatcher();

    /**
     * @brief Adds or modifies capability of **dispatchable**.
     *
     * @param di A **dispatchable** to add / modify.
     * @param can_receive Can receive capability.
     * @param can_send Can send capability.
     * @param can_disconnect Can disconnect capability.
     * @param edge_triggered Indicates if dispatch should happen in edge mode. More on edge mode of dispatch in documentation
     * of [epoll](http://man7.org/linux/man-pages/man7/epoll.7.html) and [kqueue](https://www.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2).
     */
    void add(
            const dispatchable& di,
            bool can_receive,
            bool can_send,
            bool can_disconnect,
            bool edge_triggered);
    /**
     * @brief Detaches **dispatchable** from this dispatcher.
     * @param di A **dispatchable** to detach.
     */
    void remove(const dispatchable& di);

    /**
     * @brief Dispatches a number of events from the queue to their **dispatchables**.
     * @param timeout
     * @return
     */
    template <int max_events = default_max_events>
    bool dispatch(milliseconds timeout);

    /**
     *
     * @return
     */
    template <int max_events = default_max_events>
    bool dispatch();

private:
    static const int result_error = -1;

    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) override;

    dispatcher* parent_{nullptr};
    std::unordered_set<int> dispatchables_;
};

}

#include "dispatcher.ipp"

