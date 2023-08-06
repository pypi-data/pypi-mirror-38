#pragma once

#include <chrono>
#include <ctime>
#include <tuple>


namespace framework {

template <typename ip_traits>
inline const typename packet_info<ip_traits>::endpoint_type& packet_info<ip_traits>::from() const
{
    return data_.from;
}

template <typename ip_traits>
inline std::chrono::system_clock::time_point packet_info<ip_traits>::receive_time() const
{
    return std::chrono::system_clock::time_point(
                std::chrono::seconds{data_.receive_time.tv_sec} 
              + std::chrono::nanoseconds{data_.receive_time.tv_nsec});
}

template <typename ip_traits>
inline std::chrono::system_clock::time_point packet_info<ip_traits>::read_time() const
{
    return std::chrono::system_clock::time_point(
                std::chrono::seconds{data_.read_time.tv_sec} 
              + std::chrono::nanoseconds{data_.read_time.tv_nsec});
}

template <typename ip_traits>
inline auto packet_info<ip_traits>::since() const
{
    timespec now;
    clock_gettime(CLOCK_REALTIME, &now);
    
    auto now_duration = 
            std::chrono::seconds{now.tv_sec} + 
            std::chrono::nanoseconds{now.tv_nsec};
    auto reception_duration = 
            std::chrono::seconds{data_.receive_time.tv_sec} + 
            std::chrono::nanoseconds{data_.receive_time.tv_nsec};
    auto read_duration = 
            std::chrono::seconds{data_.read_time.tv_sec} + 
            std::chrono::nanoseconds{data_.read_time.tv_nsec};
       
    using reception_duration_type = decltype(reception_duration);
    using read_duration_type = decltype(read_duration);
    using since_reception_type = decltype(now_duration - reception_duration);
    using since_read_type = decltype(now_duration - read_duration);
    return std::make_tuple(
            reception_duration != reception_duration_type::zero()
            ? now_duration - reception_duration
            : since_reception_type::zero(), 
            read_duration != read_duration_type::zero()
            ? now_duration - read_duration
            : since_read_type::zero());
}

template <typename ip_traits>
inline typename packet_info<ip_traits>::raw_data& packet_info<ip_traits>::data()
{
    return data_;
}
    
}

