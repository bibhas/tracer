# main.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'targets' : [
    {
      'target_name' : 'All',
      'type' : '<(CONTAINER)',
      'dependencies' : [
        'lldb_tracer.gyp:lldb_tracer',
        'cmio_plugin.gyp:cmioplugintracer'
      ]
    }
  ]
}
