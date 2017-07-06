# main.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'targets' : [
    {
      'target_name' : 'All',
      'type' : '<(CONTAINER)',
      'dependencies' : [
        'tracer.gyp:tracer'
      ]
    }
  ]
}
