# cmio_plugin.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'CMIO_PLUGIN_SRCROOT' : '../src/cmio_plugin/',
  },
  'targets' : [
    {
      'target_name' : 'cmioplugintracer',
      'product_name' : 'CMIOPluginTracer',
      'product_extension' : 'plugin',
      'type' : 'loadable_module',
      'mac_bundle' : 1,
      'sources' : [
        '<(CMIO_PLUGIN_SRCROOT)/plugin.mm'
      ],
      'xcode_settings' : {
        'INFOPLIST_PREPROCESS': 'NO',
        'INFOPLIST_FILE': '<(CMIO_PLUGIN_SRCROOT)/Info.plist',
      },
      'include_dirs' : [
        '<(CMIO_PLUGIN_SRCROOT)'
      ],
      'link_settings' : {
        'libraries' : [
          'CoreMediaIO.framework',
          'CoreFoundation.framework',
          'Foundation.framework'
        ]
      },
      'includes' : [
        'includes/base.gypi'
      ]
    }
  ]
}
