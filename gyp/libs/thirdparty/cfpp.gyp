# cfpp.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'SOURCE_DIR' : '../../../src'
  },
  'targets' : [
    {
      'type' : 'static_library',
      'target_name' : 'cfpp',
      'product_name' : 'cfpp',
      'sources' : [
        '<!@(ls -1 <(SOURCE_DIR)/libs/thirdparty/cfpp/CF++/source/*)'
      ],
      'include_dirs' : [
        '<(SOURCE_DIR)/libs/thirdparty/cfpp/CF++/include/',
        '<(SOURCE_DIR)/libs/thirdparty/cfpp/CF++/include/CF++'
      ],
      'all_dependent_settings' : {
        'include_dirs' : [
          '<(SOURCE_DIR)/libs/thirdparty/cfpp/CF++/include/',
          '<(SOURCE_DIR)/libs/thirdparty/cfpp/CF++/include/CF++'
        ]
      },
      'includes' : [
        '../../includes/base.gypi'
      ]
    }
  ]
}
