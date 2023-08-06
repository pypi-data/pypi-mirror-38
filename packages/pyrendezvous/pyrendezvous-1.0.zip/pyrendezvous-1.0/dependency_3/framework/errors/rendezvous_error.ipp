#pragma once

#include <system_error>


namespace framework {
    
inline rendezvous_error::rendezvous_error(
    int code,
    const std::string& what,
    error_level level)
        :
    std::system_error(std::error_code(code, std::generic_category()), what),
    level_(level)
{
    
}

inline const backtrace& rendezvous_error::where() const noexcept
{
    return where_;
}

inline error_level rendezvous_error::level() const noexcept
{
    return level_;
}

inline rendezvous_error& rendezvous_error::operator =(const rendezvous_error& other)
{
    return *this;
}

inline std::ostream& operator<<(std::ostream& os, const rendezvous_error& error)
{
    os << "rendezvous_error: " << error.what() << " at" << std::endl << error.where();
    return os;
}
    
}

