# utils.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'UTILS_LIBROOT' : '../../src/libs/utils',
  },
  'targets' : [
    {
      'target_name' : 'utils',
      'type' : '<(CONTAINER)',
      'dependencies' : [
        'libutils'
      ]
    },
    {
      'target_name' : 'libutils',
      'product_name' : 'utils',
      'type' : 'static_library',
      'include_dirs' : [
        '<(UTILS_LIBROOT)/include'
      ],
      'all_dependent_settings' : {
        'include_dirs' : [
          '<(UTILS_LIBROOT)/include'
        ]
      },
      'includes' : [
        '../includes/base.gypi'
      ]
    }
  ]
}
