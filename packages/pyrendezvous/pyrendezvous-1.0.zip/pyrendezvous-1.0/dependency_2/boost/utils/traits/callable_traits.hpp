#pragma once

#include <functional>
#include <type_traits>
#include <utility>


namespace boost { namespace utils {
  
/**
 * @brief checks if a type is a callable with the given signature.
 * 
 * @details
 * @para
 * Checks whether **tested_type** is a callable - function pointer, lambda expression
 * or functor with signature specified by **result_type** and **arg_types**. 
 * 
 * @para
 * Usage example:
 * @code
 * ...
 * 
 * static_assert(
 *          utils::is_callable<Callback, void(const Element&)>::value,
 *          "Callback has to be a callable void(const Element&)");
 * 
 * ...
 * @endcode
 */    
template <typename tested_type, typename result_type, typename... arg_types>
struct is_callable
{
    using function_type = std::function<result_type(arg_types...)>;
    
    static std::true_type test(function_type);
    static std::false_type test(...);
    
    static const bool value = 
            std::is_same<decltype(test(std::declval<tested_type>())), std::true_type>::value;
};

/**
 * @brief checks if a type is a callable with the given signature.
 * 
 * @details
 * @para
 * Checks whether **tested_type** is a callable - function pointer, lambda expression
 * or functor with signature specified by **result_type** and **arg_types**. 
 * 
 * @para
 * Usage example:
 * @code
 * ...
 * 
 * static_assert(
 *          utils::is_callable<Callback, void(const Element&)>::value,
 *          "Callback has to be a callable void(const Element&)");
 * 
 * ...
 * @endcode
 */
template <typename tested_type, typename result_type, typename... arg_types>
struct is_callable<tested_type, result_type(arg_types...)>
{
    using function_type = std::function<result_type(arg_types...)>;
    
    static std::true_type test(function_type);
    static std::false_type test(...);
    
    static const bool value = 
            std::is_same<decltype(test(std::declval<tested_type>())), std::true_type>::value;
};

template <typename T>
struct return_type : return_type<decltype(&T::operator())>
{};
// For generic types, directly use the result of the signature of its 'operator()'

template <typename ClassType, typename ReturnType, typename... Args>
struct return_type<ReturnType(ClassType::*)(Args...) const>
{
    using type = ReturnType;
};

template <typename callback_type>
struct returns_boolean
{
    using result_type = typename return_type<callback_type>::type;
    static const bool value = std::is_same<result_type, bool>::value;
};

template <
        typename callback_type,
        typename... argument_types,
        typename = typename std::enable_if<returns_boolean<callback_type>::value>::type>
bool call_with_bool_return(callback_type callback, argument_types&&... arguments)
{
    return callback(arguments...);
}

template <
        typename callback_type,
        typename... argument_types,
        typename = typename std::enable_if<!returns_boolean<callback_type>::value>::type>
bool call_with_bool_return(callback_type callback, argument_types&&... arguments, ...)
{
    callback(arguments...);
    return true;
}
    
} }
