# fakeit.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'SOURCE_DIR' : '../../../src',
  },
  'targets' : [
    {
      'type' : 'none',
      'target_name' : 'fakeit',
      'product_name' : 'fakeit',
      'include_dirs' : [
        '<(SOURCE_DIR)/libs/thirdparty/fakeit/include'
      ],
      'all_dependent_settings' : {
        'include_dirs' : [
          '<(SOURCE_DIR)/libs/thirdparty/fakeit/include'
        ]
      },
      'includes' : [
        '../../includes/base.gypi'
      ]
    }
  ]
}
