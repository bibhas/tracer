# lldb_tracer.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'LLDB_TRACER_SRCROOT' : '../src/lldb_tracer',
  },
  'targets' : [
    {
      'target_name' : 'lldb_tracer',
      'product_name' : 'lldb_tracer',
      'type' : 'executable',
      'mac_bundle' : 0,
      'sources' : [
        '<(LLDB_TRACER_SRCROOT)/tracer.mm'
      ],
      'link_settings' : {
        'libraries' : [
          'CoreFoundation.framework',
          'CoreMediaIO.framework',
          'CoreMedia.framework',
          'CoreVideo.framework',
          'CoreAudio.framework',
          'AVFoundation.framework'
        ]
      },
      'dependencies' : [
        'libs/utils.gyp:utils',
        'libs/thirdparty/lldb.gyp:lldb',
        'libs/thirdparty/cautils.gyp:cautils',
        'libs/thirdparty/cfpp.gyp:cfpp'
      ],
      'includes' : [
        'includes/base.gypi'
      ]
    }
  ]
}
