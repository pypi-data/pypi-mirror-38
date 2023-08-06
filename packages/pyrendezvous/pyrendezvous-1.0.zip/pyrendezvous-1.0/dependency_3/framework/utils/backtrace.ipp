#pragma once

#include <cerrno>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>

#include <execinfo.h>


namespace framework {

inline backtrace::backtrace()
{
    nptrs_ = ::backtrace(buffer_, BT_BUF_SIZE);
    locations_ = ::backtrace_symbols(buffer_, nptrs_);
    if (locations_ == NULL)
    {
        auto error = strerror(errno);
        throw std::runtime_error(error);
    }
}

inline backtrace::backtrace(const backtrace& other)
        :
    nptrs_(other.nptrs_)
{
    locations_ = ::backtrace_symbols(buffer_, nptrs_);
}

inline backtrace::~backtrace()
{
    free(locations_);
}

inline std::ostream& operator<<(std::ostream& os, const backtrace& bt)
{
    for (auto j = 0ul; j < bt.nptrs_; j++)
        os << bt.locations_[j] << std::endl;
    return os;
}

}

