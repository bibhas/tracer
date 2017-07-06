// stracc.h
// 2017 Bibhas Acharya <mail@bibhas.com>

#pragma once

#include <sstream>

template<typename T>
inline void stracc_impl(std::ostringstream& ss, const T&& t) {
  ss << std::string(t);
}

template<typename T, typename ...Args>
inline void stracc_impl(std::ostringstream& ss, const T&& t, Args&& ...args) {
  ss << std::string(t); 
  stracc_impl(ss, std::move(args)...);
}

template<typename ...Args>
inline std::string stracc(Args&& ...args) {
  std::ostringstream ss;
  stracc_impl(ss, std::move(args)...);
  return ss.str();
}

