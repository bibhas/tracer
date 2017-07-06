// fourchar.h
// 2017 Bibhas Acharya <mail@bibhas.com>

#include <string>
#include <sstream>
#include <TargetConditionals.h>
#include <utils/compute.h>

static inline std::string IntToFourCharString(int value) {
  union {
    unsigned int value;
    unsigned char bytes[4];
  } repr;
  repr.value = value;
  std::ostringstream ostr = COMPUTE({
    std::ostringstream resp;
#if TARGET_RT_BIG_ENDIAN
    for (int i = 0; i < 4; i++) {
#else
    for (int i = 3; i >= 0; i--) {
#endif
      resp << (unsigned char)repr.bytes[i];
    }
    return resp;
  });
  return ostr.str();
}

