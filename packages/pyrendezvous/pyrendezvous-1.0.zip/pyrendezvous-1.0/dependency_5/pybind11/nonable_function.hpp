#pragma once

#include <pybind11/pybind11.h>

#include <functional>


namespace pybind11 {
    
inline int PyCallableOrNone_Check(PyObject *o)
{
    if (o == Py_None)
        return 1;
    else
        return PyCallable_Check(o);
}

template <typename... args>
class nonable_function : public function {
public:
    PYBIND11_OBJECT_DEFAULT(nonable_function<args...>, function, PyCallableOrNone_Check)
          
    operator std::function<void(args...)>() const
    {
        if (!is_none())
            return static_cast<function>(*this);
        
        std::function<void(args...)> empty;
        return empty;
    }
};
    
}
