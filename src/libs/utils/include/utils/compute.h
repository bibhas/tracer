// compute.h
// 2017 Bibhas Acharya <mail@bibhas.com>

#pragma once

// This is an overloaded set of COMPUTE pp functions. Usage:
//
// // COMPUTE(float, { return 1.0f }); OR <- Explicit return type declaration
//
// // COMPUTE({ return 1.0f }); <- Return type deduced (C++14)

#define OVERLOADED_MACRO(M, ...) _OVR(M, _COUNT_ARGS(__VA_ARGS__)) (__VA_ARGS__)

#define _OVR(macroName, number_of_args)   _OVR_EXPAND(macroName, number_of_args)

#define _OVR_EXPAND(macroName, number_of_args)    macroName##number_of_args

#define _COUNT_ARGS(...) _ARG_PATTERN_MATCH(__VA_ARGS__, 9,8,7,6,5,4,3,2,1)

#define _ARG_PATTERN_MATCH(_1,_2,_3,_4,_5,_6,_7,_8,_9, N, ...)   N

#define COMPUTE(...) OVERLOADED_MACRO(COMPUTE, __VA_ARGS__)

#define COMPUTE1(F) ([&]F)()

#define COMPUTE2(R, F) ([&]()-> R F)()
