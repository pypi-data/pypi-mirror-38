#pragma once

#include <cerrno>
#include <chrono>
#include <cstring>
#include <sys/epoll.h>
#include <unistd.h>
#include <utility>


namespace framework {

inline dispatcher::dispatcher(error_callback_type error_callback)
        :
    dispatchable(error_callback)
{
    auto epoll_fd = ::epoll_create1(0);
    check_lethal_error(epoll_fd);

    dispatchable::set_fd(epoll_fd);
}

inline dispatcher::dispatcher(
    dispatcher& parent,
    error_callback_type error_callback)
        :
    dispatcher(error_callback)
{
    parent_ = &parent;
    parent.add(*this, true, false, false, false);
}

inline dispatcher::~dispatcher()
{
    if (parent_ != nullptr)
        parent_->remove(*this);
}

inline void dispatcher::add(
        const dispatchable& tr,
        bool can_receive,
        bool can_send,
        bool can_disconnect,
        bool edge_triggered)
{
    epoll_event event{};
    if (can_receive)
        event.events |= EPOLLIN;
    if (can_send)
        event.events |= EPOLLOUT;
    if (can_disconnect)
        event.events |= EPOLLHUP;
    if (edge_triggered)
        event.events |= EPOLLET;
    event.data.fd = tr.fd();
    event.data.ptr = const_cast<dispatchable*>(&tr);

    auto operation = EPOLL_CTL_MOD;
    if (dispatchables_.find(tr.fd()) == dispatchables_.end())
    {
        dispatchables_.emplace(tr.fd());
        operation = EPOLL_CTL_ADD;
    }

    auto ctl_result = ::epoll_ctl(fd(), operation, tr.fd(), &event);
    check_error(ctl_result);
}

inline void dispatcher::remove(const dispatchable& tr)
{
    auto search_result = dispatchables_.find(tr.fd());
    if (search_result != dispatchables_.end())
    {
        dispatchables_.erase(search_result);

        epoll_event event{};
        auto ctl_result = ::epoll_ctl(fd(), EPOLL_CTL_DEL, tr.fd(), &event);
        check_error(ctl_result);
    }
}

template <int max_events>
inline bool dispatcher::dispatch(milliseconds timeout)
{
    epoll_event events[max_events];
    auto wait_result = ::epoll_wait(fd(), events, max_events, timeout.count());
    check_error(wait_result);

    if (wait_result == 0)
        return false;

    for (auto i = 0; i < wait_result; i++)
    {
        auto& event = events[i];
        auto target = reinterpret_cast<dispatchable*>(event.data.ptr);

        target->handle_event(
                (event.events & EPOLLIN) == EPOLLIN,
                (event.events & EPOLLOUT) == EPOLLOUT,
                (event.events & EPOLLHUP) == EPOLLHUP);
    }

    return true;
}

template <int max_events>
inline bool dispatcher::dispatch()
{
    return dispatch<max_events>(milliseconds::zero());
}

inline void dispatcher::handle_event(
        bool should_receive,
        bool should_send,
        bool should_disconnect)
{
    dispatch(milliseconds::zero());
}

}

