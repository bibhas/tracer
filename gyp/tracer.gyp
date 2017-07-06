# tracer.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'TRACER_SRCROOT' : '../src/tracer',
  },
  'targets' : [
    {
      'target_name' : 'tracer',
      'product_name' : 'tracer',
      'type' : 'executable',
      'mac_bundle' : 0,
      'sources' : [
        '<(TRACER_SRCROOT)/tracer.mm'
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
        'libs/thirdparty/cautils.gyp:cautils',
        'libs/thirdparty/cfpp.gyp:cfpp'
      ],
      'includes' : [
        'includes/base.gypi'
      ]
    }
  ]
}
