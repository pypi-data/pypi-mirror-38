#pragma once

#include <string>
#include <vector>

namespace framework {

namespace string_utils {

/**
 * @brief Returns a string vector that contains the substrings in this instance that
 * are delimited by the **separator**.
 *
 * @details
 * @para
 * Split is used to break a delimited string into substrings.
 *
 * @para
 * The Split method is not always the best way to break a delimited string into
 * substrings. If you don't want to extract all of the substrings of a delimited
 * string, or if you want to parse a string based on a pattern instead of a set
 * of delimiter characters, consider the following alternatives.
 *
 * @param s A string to split.
 * @param seperator A delimeter to split the string at.
 * @return A vector of substrings. If **separator** is not present in the string,
 * the whole input string is placed as the only element of returned vector.
 */
std::vector<std::string> split(const std::string& s, char seperator);

}

}

#include "string_utils.ipp"

