#pragma once

#include <random>
#include <sstream>
#include <string>


namespace boost { namespace utils {

/**
 * @brief A simplified interface for random data generation. 
 * 
 * @details
 * This class is intended to be used by library's unit tests only. 
 */    
class random
{
public:
    static std::string generate(std::size_t size)
    {
        std::mt19937 generator;
        std::uniform_int_distribution<std::size_t> distribution(0ul, strlen(RANDOM_ALLOWED_CHARACTERS) - 1);
        
        std::stringstream ss;
        for (auto i = 0ul; i < size; i++)
            ss << RANDOM_ALLOWED_CHARACTERS[distribution(generator)];
        
        return ss.str();
    }
    
private:
    static constexpr auto RANDOM_ALLOWED_CHARACTERS = 
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890";
};

} }

