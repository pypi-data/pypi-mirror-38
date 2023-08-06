#pragma once

#include <cstdint>


namespace framework {

enum class error_level : uint8_t
{
    non_lethal = 0,
    lethal = 1
};     
    
}
