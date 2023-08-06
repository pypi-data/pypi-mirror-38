#pragma once

#include <pybind11/pybind11.h>


namespace pybind11 {
    
template <return_value_policy policy>
class set_return_policy
{
public:
    set_return_policy(function target)
        : target_(target)
    {
        
    }
        
    template <typename... arg_types>
    object operator()(arg_types&&... args) const
    {
        return target_.operator ()<policy>(args...);
    }
    
private:
    function target_;
};

using set_reference_return_policy = set_return_policy<return_value_policy::reference>;
    
}

