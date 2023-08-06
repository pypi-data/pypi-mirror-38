#pragma once

#include <framework/errors/error_level.hpp>
#include <framework/utils/backtrace.hpp>

#include <exception>
#include <iostream>
#include <string>
#include <system_error>


namespace framework {

/**
 * @brief Represents a **std::system_error** originated from within this framework.
 *
 * @details
 * @para
 * **rendezvous_error** extends **std::system_error** with two attributes:
 * **where**, serving backtrace of error occurance and **level**, showing severity of
 * the error.
 *
 * @para
 * It's recommended to use **error_handler** for raising **rendezvous_error**.
 */
class rendezvous_error : public std::system_error
{
public:
    /**
     * @brief Initializes an instance of **rendezvous_error**.
     * @param code Error code.
     * @param what Error description message.
     * @param level Error level.
     */
    explicit rendezvous_error(
            int code,
            const std::string& what,
            error_level level = error_level::non_lethal);

    /**
     * @brief Returns the backtrace of where the error occured.
     * @return The backtrace string.
     */
    const backtrace& where() const noexcept;

    /**
     * @brief Returns the error level.
     * @return Either lethal or non-lethal error.
     */
    error_level level() const noexcept;

    /**
     * @brief Copy assignable.
     */
    rendezvous_error& operator=(const rendezvous_error& other);

private:
    backtrace where_;
    error_level level_;
};

std::ostream& operator<<(std::ostream& os, const rendezvous_error& error);

}

#include "rendezvous_error.ipp"
