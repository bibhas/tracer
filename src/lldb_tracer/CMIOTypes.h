// CMIOTypes.h
// 2017 Bibhas Acharya <mail@bibhas.com>

#pragma once

static inline std::string tryTranslateSelectorName(std::uint32_t selectorValue) {
  switch (selectorValue) {
    // Stream Properties
    case 'sdir': {
      return std::string("kCMIOStreamPropertyDirection");
    }
    case 'term': {
      return std::string("kCMIOStreamPropertyTerminalType");
    }
    case 'schn': {
      return std::string("kCMIOStreamPropertyStartingChannel");
    }
    case 'ltnc': {
      return std::string("kCMIOStreamPropertyLatency OR kCMIODevicePropertyLatency");
    }
    case 'pft ': {
      return std::string("kCMIOStreamPropertyFormatDescription");
    }
    case 'pfta': {
      return std::string("kCMIOStreamPropertyFormatDescriptions");
    }
    case 'stmg': {
      return std::string("kCMIOStreamPropertyStillImage");
    }
    case 'stft': {
      return std::string("kCMIOStreamPropertyStillImageFormatDescriptions");
    }
    case 'nfrt': {
      return std::string("kCMIOStreamPropertyFrameRate");
    }
    case 'mfrt': {
      return std::string("kCMIOStreamPropertyMinimumFrameRate");
    }
    case 'nfr#': {
      return std::string("kCMIOStreamPropertyFrameRates");
    }
    case 'frrg': {
      return std::string("kCMIOStreamPropertyFrameRateRanges");
    }
    case 'pmn1': {
      return std::string("kCMIOStreamPropertyNoDataTimeoutInMSec");
    }
    case 'pmn2': {
      return std::string("kCMIOStreamPropertyDeviceSyncTimeoutInMSec");
    }
    case 'pmn3': {
      return std::string("kCMIOStreamPropertyNoDataEventCount");
    }
    case 'pmou': {
      return std::string("kCMIOStreamPropertyOutputBufferUnderrunCount");
    }
    case 'pmor': {
      return std::string("kCMIOStreamPropertyOutputBufferRepeatCount");
    }
    case 'pmoq': {
      return std::string("kCMIOStreamPropertyOutputBufferQueueSize");
    }
    case 'pmos': {
      return std::string("kCMIOStreamPropertyOutputBuffersRequiredForStartup");
    }
    case 'miff': {
      return std::string("kCMIOStreamPropertyOutputBuffersNeededForThrottledPlayback");
    }
    case 'popt': {
      return std::string("kCMIOStreamPropertyFirstOutputPresentationTimeStamp");
    }
    case 'pmed': {
      return std::string("kCMIOStreamPropertyEndOfData");
    }
    case 'pmcl': {
      return std::string("kCMIOStreamPropertyClock");
    }
    case 'pdcd': {
      return std::string("kCMIOStreamPropertyCanProcessDeckCommand");
    }
    case 'deck': {
      return std::string("kCMIOStreamPropertyDeck");
    }
    case 'tcod': {
      return std::string("kCMIOStreamPropertyDeckFrameNumber");
    }
    case 'drop': {
      return std::string("kCMIOStreamPropertyDeckDropness");
    }
    case 'thrd': {
      return std::string("kCMIOStreamPropertyDeckThreaded");
    }
    case 'locl': {
      return std::string("kCMIOStreamPropertyDeckLocal");
    }
    case 'cuec': {
      return std::string("kCMIOStreamPropertyDeckCueing");
    }
    case 'ipls': {
      return std::string("kCMIOStreamPropertyInitialPresentationTimeStampForLinkedAndSyncedAudio");
    }
    case 'sonp': {
      return std::string("kCMIOStreamPropertyScheduledOutputNotificationProc");
    }
    case 'prfd': {
      return std::string("kCMIOStreamPropertyPreferredFormatDescription");
    }
    case 'prfr': {
      return std::string("kCMIOStreamPropertyPreferredFrameRate");
    }
    // Device properties
    case 'plug': {
      return std::string("kCMIODevicePropertyPlugIn");
    }
    case 'uid ': {
      return std::string("kCMIODevicePropertyDeviceUID");
    }
    case 'muid': {
      return std::string("kCMIODevicePropertyModelUID");
    }
    case 'tran': {
      return std::string("kCMIODevicePropertyTransportType");
    }
    case 'livn': {
      return std::string("kCMIODevicePropertyDeviceIsAlive");
    }
    case 'diff': {
      return std::string("kCMIODevicePropertyDeviceHasChanged");
    }
    case 'goin': {
      return std::string("kCMIODevicePropertyDeviceIsRunning");
    }
    case 'gone': {
      return std::string("kCMIODevicePropertyDeviceIsRunningSomewhere");
    }
    case 'dflt': {
      return std::string("kCMIODevicePropertyDeviceCanBeDefaultDevice");
    }
    case 'oink': {
      return std::string("kCMIODevicePropertyHogMode");
    }
    /*case 'ltnc': {
      return std::string("kCMIODevicePropertyLatency");
    }*/
    case 'stm#': {
      return std::string("kCMIODevicePropertyStreams");
    }
    case 'slay': {
      return std::string("kCMIODevicePropertyStreamConfiguration");
    }
    case 'pmnh': {
      return std::string("kCMIODevicePropertyDeviceMaster");
    }
    case 'ixna': {
      return std::string("kCMIODevicePropertyExcludeNonDALAccess");
    }
    case 'pmcs': {
      return std::string("kCMIODevicePropertyClientSyncDiscontinuity");
    }
    case 'pmsc': {
      return std::string("kCMIODevicePropertySMPTETimeCallback");
    }
    case 'pmac': {
      return std::string("kCMIODevicePropertyCanProcessAVCCommand");
    }
    case 'pmat': {
      return std::string("kCMIODevicePropertyAVCDeviceType");
    }
    case 'pmsm': {
      return std::string("kCMIODevicePropertyAVCDeviceSignalMode");
    }
    case 'r422': {
      return std::string("kCMIODevicePropertyCanProcessRS422Command");
    }
    case 'plud': {
      return std::string("kCMIODevicePropertyLinkedCoreAudioDeviceUID");
    }
    case 'vdig': {
      return std::string("kCMIODevicePropertyVideoDigitizerComponents");
    }
    case 'sbyu': {
      return std::string("kCMIODevicePropertySuspendedByUser");
    }
    case 'plsd': {
      return std::string("kCMIODevicePropertyLinkedAndSyncedCoreAudioDeviceUID");
    }
    case 'iuns': {
      return std::string("kCMIODevicePropertyIIDCInitialUnitSpace");
    }
    case 'csrd': {
      return std::string("kCMIODevicePropertyIIDCCSRData");
    }
    case 'frnd': {
      return std::string("kCMIODevicePropertyCanSwitchFrameRatesWithoutFrameDrops");
    }
    // Object properties
    case 'clas': {
      return std::string("kCMIOObjectPropertyClass");
    }
    case 'stdv': {
      return std::string("kCMIOObjectPropertyOwner");
    }
    case 'oplg': {
      return std::string("kCMIOObjectPropertyCreator");
    }
    case 'lnam': {
      return std::string("kCMIOObjectPropertyName");
    }
    case 'lmak': {
      return std::string("kCMIOObjectPropertyManufacturer");
    }
    case 'lchn': {
      return std::string("kCMIOObjectPropertyElementName");
    }
    case 'lccn': {
      return std::string("kCMIOObjectPropertyElementCategoryName");
    }
    case 'lcnn': {
      return std::string("kCMIOObjectPropertyElementNumberName");
    }
    case 'ownd': {
      return std::string("kCMIOObjectPropertyOwnedObjects");
    }
    case 'lisa': {
      return std::string("kCMIOObjectPropertyListenerAdded");
    }
    case 'lisr': {
      return std::string("kCMIOObjectPropertyListenerRemoved");
    }
    // System object properties
    case 'mast': {
      return std::string("kCMIOHardwarePropertyProcessIsMaster");
    }
    case 'inot': {
      return std::string("kCMIOHardwarePropertyIsInitingOrExiting");
    }
    case 'dev#': {
      return std::string("kCMIOHardwarePropertyDevices");
    }
    case 'dIn ': {
      return std::string("kCMIOHardwarePropertyDefaultInputDevice");
    }
    case 'dOut': {
      return std::string("kCMIOHardwarePropertyDefaultOutputDevice");
    }
    case 'duid': {
      return std::string("kCMIOHardwarePropertyDeviceForUID");
    }
    case 'slep': {
      return std::string("kCMIOHardwarePropertySleepingIsAllowed");
    }
    case 'unld': {
      return std::string("kCMIOHardwarePropertyUnloadingIsAllowed");
    }
    case 'pibi': {
      return std::string("kCMIOHardwarePropertyPlugInForBundleID");
    }
    case 'user': {
      return std::string("kCMIOHardwarePropertyUserSessionIsActiveOrHeadless");
    }
    case 'sbys': {
      return std::string("kCMIOHardwarePropertySuspendedBySystem");
    }
    case 'yes ' : {
      return std::string("kCMIOHardwarePropertyAllowScreenCaptureDevices");
    }
    // Default
    default: {
      return "Unknown";
    }
  }
}

static inline std::string tryTranslateScopeName(std::uint32_t scopeName) {
  switch (scopeName) {
    case 'inpt': {
      return std::string("kCMIODevicePropertyScopeInput");
    }
    case 'outp': {
      return std::string("kCMIODevicePropertyScopeOutput");
    }
    case 'ptru': {
      return std::string("kCMIODevicePropertyScopePlayThrough");
    }
    case 'adev': {
      return std::string("kCMIODeviceClassID");
    }
    default: {
      return std::string("Unknown");
    }
 }                
}

static inline std::string tryTranslateElementName(std::uint32_t elemName) {
  switch (elemName) {
    case 0UL: {
      return std::string("kCMIOObjectPropertyElementMaster");
    }
    default: {
      return std::string("Unknown");
    }
  }
}
