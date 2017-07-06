# includes/mac.gypi
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'xcode_settings' : {
    'ARCHS': [ 'x86_64' ],
    'SDKROOT': 'macosx<(macos_sdk_version)',
    'MACOSX_DEPLOYMENT_TARGET': '10.12',
    'DEBUG_INFORMATION_FORMAT': 'dwarf-with-dsym',
    'DEPLOYMENT_POSTPROCESSING': 'YES',
    'DEAD_CODE_STRIPPING' : 'YES',
    'GCC_GENERATE_DEBUGGING_SYMBOLS' : 'YES',
    'OTHER_CFLAGS' : [
      '-fcolor-diagnostics',
      '-Wno-unused-variable',
      '-Wno-unused-parameter',
      '-Wno-padded',
      '-g'
    ],
    'OTHER_CPLUSPLUSFLAGS' : [
      '-fcolor-diagnostics',
      '-std=c++14',
      '-fobjc-call-cxx-cdtors',
      '-fms-extensions',
      '-stdlib=libc++',
      '-Wmicrosoft-template',
      '-Wno-unused-variable',
      '-Wno-unused-parameter',
      '-Wno-c++98-compat',
      '-Wno-c++98-compat-pedantic',
      '-Wno-padded',
      '-Wno-gnu-zero-variadic-macro-arguments',
      '-g'
    ],
  }
}

