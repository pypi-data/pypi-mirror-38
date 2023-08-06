#pragma once

#include <framework/dispatchable.hpp>

#include <functional>


namespace framework {

/**
 * @brief Base type for all transports.
 *
 * @details
 * **transport** type currently doesn't do much, except indication which type is
 * a transport.
 */
class transport : public dispatchable
{
protected:
    /**
     * @brief Initializes the base **transport**.
     * @param error_callback A callback invoked for non-lethal errors.
     */
    transport(error_callback_type error_callback);
    /**
     * @breif Called upon destruction.
     */
    virtual ~transport();

    /**
     * @brief Checks if underlying file descriptor is valid.
     */
    void throw_on_wrong_fd();

};

}

#include "transport.ipp"
