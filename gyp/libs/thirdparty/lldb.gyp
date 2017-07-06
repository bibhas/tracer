# lldb.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'LLDB_LIBROOT' : '../../../src/libs/thirdparty/lldb',
  },
  'targets' : [
    {
      'target_name' : 'lldb',
      'type' : '<(CONTAINER)',
      'direct_dependent_settings' : {
        'include_dirs' : [
          '<(LLDB_LIBROOT)/include'
        ],
        'link_settings' : {
          'libraries' : [
            'LLDB.framework'
          ]
        },
        'xcode_settings' : {
          'OTHER_LDFLAGS' : [
            '-F/Applications/Xcode.app/Contents/SharedFrameworks',
            '-Wl,-rpath "/Applications/Xcode.app/Contents/SharedFrameworks"'
          ]
        }
      }
    }
  ]
}
