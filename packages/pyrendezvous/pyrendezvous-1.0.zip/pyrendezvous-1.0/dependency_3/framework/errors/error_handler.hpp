#pragma once

#include <framework/errors/error_level.hpp>

#include <functional>


namespace framework {

/**
 * @brief Contains helper methods to selectively raise error of given type.
 *
 * @details
 * @para
 * Many components in this framework interact with system functions. These functions
 * report errors through error codes. This class provides facilities for:
 * * filtering error results from non error results of system calls
 * * conversion of system errors into **error_type**
 * * raising the error through supplementary mechanisms based on their availability
 * and error severity.
 *
 * @para
 * Error handler facilitates error notification through an **error callback** whenever
 * a valid, defined callback is passed to it during its construction. Only non-lethal
 * errors are reported through the callback. In case an error is lethal or callback
 * isn't defined, c++ exception mechanism is used for reporting.
 */
template <typename error_type>
class error_handler
{
protected:
    using error_callback_type = std::function<void(error_type&)>;

    /**
     * @brief Initializes an **error_handler**.
     * @param error_callback A callback through which non lethal errors should be reported.
     */
    error_handler(error_callback_type error_callback);

    /**
     * @brief Unconditionally raises an error with the given code.
     * @param error_code An error code for the raised error.
     */
    template <error_level level = error_level::non_lethal>
    void raise_error(int error_code) const;

    /**
     * @brief Checks if the result indicates an error, if so raise a lethal error.
     * @param result A result to check.
     * @return **true** if result is not an error, **false** otherwise.
     */
    template <typename result_type, error_level level = error_level::non_lethal>
    bool check_error(result_type result) const;

    /**
     * @brief Checks if the result indicates an error, if so raise a lethal error.
     *
     * @details
     * If result is an error, a lethal error will be raised.
     * @param result A result to check.
     * @return **true** if result is not an error, **false** otherwise.
     */
    template <typename result_type>
    bool check_lethal_error(result_type result) const;

private:
    static const int result_error = -1;

    error_callback_type error_callback_;
};

}

#include "error_handler.ipp"

