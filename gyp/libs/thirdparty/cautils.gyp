# cautils.gyp
# 2017 Bibhas Acharya <mail@bibhas.com>

{
  'variables' : {
    'SOURCE_DIR' : '../../../src'
  },
  'targets' : [
    {
      'type' : 'static_library',
      'target_name' : 'cautils',
      'product_name' : 'cautils',
      'sources' : [
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/AUOutputBL.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/AUParamInfo.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAUParameter.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAUProcessor.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAudioBufferList.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAudioChannelLayout.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAudioChannelLayoutObject.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAudioFileFormats.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAAudioValueRange.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CABufferList.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CABundleLocker.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFArray.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFDictionary.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFDistributedNotification.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFMachPort.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFMessagePort.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFNumber.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFPreferences.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CACFString.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAComponent.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAComponentDescription.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CADebugMacros.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CADebugPrintf.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CADebugger.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAGuard.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAHALAudioDevice.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAHALAudioObject.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAHALAudioStream.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAHALAudioSystemObject.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAHostTimeBase.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAMutex.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAPThread.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAPersistence.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAProcess.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CARingBuffer.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CASettingsStorage.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CASharedLibrary.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CASpectralProcessor.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAStreamBasicDescription.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAStreamRangedDescription.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAVectorUnit.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAVolumeCurve.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/CAXException.cpp',
        '<(SOURCE_DIR)/libs/thirdparty/cautils/PublicUtility/MatrixMixerVolumes.cpp'
      ],
      'include_dirs' : [
        '<(SOURCE_DIR)/libs/thirdparty/cautils',
      ],
      'all_dependent_settings' : {
        'include_dirs' : [
          '<(SOURCE_DIR)',
          '<(SOURCE_DIR)/libs',
          '<(SOURCE_DIR)/libs/thirdparty/cautils',
        ],
        'link_settings' : {
          'libraries' : [
            'CoreFoundation.framework',
            'CoreAudio.framework'
          ]
        }
      },
      'includes' : [
        '../../includes/base.gypi'
      ]
    }
  ]
}
