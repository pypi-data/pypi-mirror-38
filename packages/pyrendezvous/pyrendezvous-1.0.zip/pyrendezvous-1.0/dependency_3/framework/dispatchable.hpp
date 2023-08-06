#pragma once

#include <framework/errors/error_handler.hpp>
#include <framework/errors/rendezvous_error.hpp>

#include <system_error>


namespace framework {

/**
 * @brief A recipient of notifications dispatched by a **dispatcher**.
 *
 * @details
 *
 */
class dispatchable : protected error_handler<rendezvous_error>
{
public:
    /**
     * @brief Non-trivially constructable.
     */
    dispatchable() = delete;
    /**
     * @brief Non-copy constructable.
     * @param other
     */
    dispatchable(const dispatchable& other) = delete;
    /**
     * @brief Non-move constructable.
     * @param other
     */
    dispatchable(dispatchable&& other) = delete;

    /**
     * @brief Handles an event dispatched by a **dispatcher**.
     *
     * @details
     * The event defines what sort of I/O operation the file descriptor represented
     * by this **dospatchable** is ready for.
     *
     * @param should_receive Indicates readiness for read.
     * @param should_send Indicates readiness for write.
     * @param should_disconnect Indicates disconnection.
     */
    virtual void handle_event(
            bool should_receive,
            bool should_send,
            bool should_disconnect) = 0;
    /**
     * @brief Obtains underlying file descriptor.
     *
     * @details
     * @para
     * A **dispatchable** holds ownership over a file, device, socket or any other
     * system resource which can be registered for event dispatch. All those resources
     * are indicated in the system as file descriptor. This method acts as an accessor
     * to that descriptor.
     *
     * @para
     * A valid file descriptor is a positive integer. 0 indicates a **dispatchable**
     * which doesn't own an open system resource which can be dispatched.
     *
     * @para
     * A file descriptor can be set by a descendant only with **set_fd** method.
     *
     * @return A file descriptor.
     */
    int fd() const;

protected:
    using rendezvous_error_handler = error_handler<rendezvous_error>;

    /**
     * @brief To be set in condition when a **dispatchable** doesn't own a file descriptor.
     */
    static const int no_fd = 0;

    /**
     * @brief Creates an instance of a **dispatchable**.
     * @param error_callback A callback used for reporting errors.
     */
    dispatchable(error_callback_type error_callback = {});
    /**
     * @brief Called upon destruction.
     */
    virtual ~dispatchable();

    /**
     * @brief Sets the underlying file descriptor.
     * @param fd The file descriptor to set or @see no_fd.
     */
    void set_fd(int fd);

private:
    int fd_ {no_fd};

};

}

#include "dispatchable.ipp"

