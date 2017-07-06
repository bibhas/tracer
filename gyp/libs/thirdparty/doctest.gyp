# doctest.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'SOURCE_DIR' : '../../../src'
  },
  'targets' : [
    {
      'type' : 'none',
      'target_name' : 'doctest',
      'product_name' : 'doctest',
      'sources' : [
        '<(SOURCE_DIR)/libs/thirdparty/doctest/src/doctest/doctest.h',
        '<(SOURCE_DIR)/libs/thirdparty/doctest/src/doctest/parts/*'
      ],
      'all_dependent_settings' : {
        'include_dirs' : [
          '<(SOURCE_DIR)/libs/thirdparty/doctest/include'
        ]
      },
      'includes' : [
        '../../includes/base.gypi'
      ]
    }
  ]
}
