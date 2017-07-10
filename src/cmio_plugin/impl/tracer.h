// tracer.h
// 2017 Bibhas Acharya <mail@bibhas.com>

#include <iostream>
#include <CoreMediaIO/CMIOHardwarePlugIn.h>

static CMIOHardwarePlugInInterface cachedInterface;
static CMIOHardwarePlugInInterface newInterface;

void *CMIOPluginTracerGetHookedInterface(void* (*func_ptr)(CFAllocatorRef, CFUUIDRef), CFAllocatorRef allocator, CFUUIDRef requestedTypeUUID) {
  std::cout << "Inside interface..." << std::endl;
  CMIOHardwarePlugInInterface *interface = static_cast<CMIOHardwarePlugInInterface *>(
    func_ptr(allocator, requestedTypeUUID)
  );
  cachedInterface = *interface;
  newInterface = *interface;
  newInterface.QueryInterface = [](void* _self, REFIID _uuid, LPVOID* _interface) -> HRESULT {
    std::cout << "Asking QueryInterface..." << std::endl;
    HRESULT resp = cachedInterface.QueryInterface(_self, _uuid, _interface);
    std::cout << "Returned from QueryInterface..." << std::endl;
    return resp;
  };
  newInterface.ObjectHasProperty = [](CMIOHardwarePlugInRef _self, CMIOObjectID _objectID, const CMIOObjectPropertyAddress* _address) -> Boolean {
    std::cout << "Asking ObjectHasProperty..." << std::endl;
    Boolean resp = cachedInterface.ObjectHasProperty(_self, _objectID, _address);
    std::cout << "Returned from ObjectHasProperty..." << std::endl;
    return resp;
  };
  newInterface.ObjectGetPropertyData = [](
    CMIOHardwarePlugInRef self, 
    CMIOObjectID objectID, 
    const CMIOObjectPropertyAddress* address, 
    UInt32 qualifierDataSize, 
    const void* qualifierData, 
    UInt32 dataSize, 
    UInt32* dataUsed, 
    void* data) -> OSStatus {
      std::cout << "Asked ObjectHasProperty..." << std::endl;
      return cachedInterface.ObjectGetPropertyData(self, objectID, address, qualifierDataSize, qualifierData, dataSize, dataUsed, data);
  };
  newInterface.ObjectGetPropertyDataSize = [](   CMIOHardwarePlugInRef               self,
                                    CMIOObjectID                        objectID,
                                    const CMIOObjectPropertyAddress*    address,
                                    UInt32                              qualifierDataSize,
                                    const void*                         qualifierData,
                                    UInt32*                             dataSize) -> OSStatus {
  
      std::cout << "Asked ObjectGetPropertyDataSize..." << std::endl;
      return noErr;
  };
  std::cout << "Returning from interface..." << std::endl;
  return &newInterface;
}

