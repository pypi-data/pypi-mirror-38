#pragma once

#include <stdexcept>


namespace framework {

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::protocol_reassembler(
        callback_type callback)
    :
        partial_(),
        callback_(callback)
{

}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
void protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::operator ()(
        source_type& source,
        boost::memory::buffer_ref& buffer)
{
    auto current = buffer.as_pointer<uint8_t*>();
    auto end = buffer.as_pointer<uint8_t*>() + buffer.length();

    // handle a partial at the beginning
    if (partial_.length() > 0ul)
    {
        auto initial_partial_size = partial_.length();
        partial_.append(buffer.as_pointer<void*>(), buffer.length());

        auto complete_size = protocol_traits::complete_size(*partial_);
        if (complete_size == 0)
            return;

        auto complement_size = complete_size - initial_partial_size;
        current += complement_size;

        auto message = *partial_;
        callback_(source, message);
        partial_.reset();
    }

    // handle full messages
    while (true)
    {
        auto remaining_size = end - current;
        if (remaining_size == 0)
            return;

        boost::memory::buffer_ref data(current, remaining_size);
        auto complete_size = protocol_traits::complete_size(std::move(data));

        if (complete_size == 0 || remaining_size < complete_size)
        {
            partial_.append(current, remaining_size);
            return;
        }

        boost::memory::buffer_ref message(current, complete_size);
        callback_(source, message);
        current += complete_size;
    }
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
void protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::operator ()(
        source_type& source,
        boost::memory::buffer_ref&& buffer)
{
    auto& enforced_ref = buffer;
    operator ()(source, enforced_ref);
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
bool protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::unfinished() const
{
    return partial_.length() > 0ul;
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
inline protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::partial::partial()
{
    data_ = std::malloc(initial_capacity);
    if (data_ == nullptr)
        throw std::system_error(
                std::error_code(errno, std::generic_category()));
    capacity_ = initial_capacity;
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
inline protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::partial::~partial()
{
    if (data_ != nullptr)
        std::free(data_);
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
inline void protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::partial::append(void* data, size_t length)
{
    if (capacity_ - position_ < length)
    {
        auto new_capacity = capacity_ * 2ul;
        if (new_capacity > partial_limit)
            throw std::length_error("partial limit reached!");
        
        auto new_data = std::realloc(data_, new_capacity);
        if (new_data == nullptr)
            throw std::system_error(
                std::error_code(errno, std::generic_category()));

        data_ = new_data;
        capacity_ = new_capacity;
    }

    std::memcpy(reinterpret_cast<uint8_t*>(data_) + position_, data, length);
    position_ += length;
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
inline void protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::partial::reset()
{
    position_ = 0ul;
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
inline boost::memory::buffer_ref protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::partial::operator*() const
{
    return boost::memory::buffer_ref(reinterpret_cast<uint8_t*>(data_), position_);
}

template <
        typename source_type,
        typename protocol_traits,
        size_t partial_limit>
inline size_t protocol_reassembler<
        source_type,
        protocol_traits,
        partial_limit>::partial::length() const
{
    return position_;
}

}