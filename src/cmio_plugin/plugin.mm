// plugin.mm
// 2017 Bibhas Acharya <mail@bibhas.com>

#include <CoreFoundation/CoreFoundation.h>
#include "impl/tracer.h"

extern "C" {
  // Expose entry point for our plugin
  void* CMIOPluginTracerGetInterface(CFAllocatorRef allocator, CFUUIDRef requestedTypeUUID) {
    const char *pluginPath = "/Library/CoreMediaIO/Plug-Ins/DAL/iGlasses.plugin";
    NSURL *pluginURL = [NSURL fileURLWithPath:[NSString stringWithFormat:@"%s", pluginPath]];
    CFBundleRef pluginBundle = CFBundleCreate(kCFAllocatorDefault, (CFURLRef)pluginURL);
    assert(pluginBundle && "Could not create plugin bundle!");
    void* (*func_ptr)(CFAllocatorRef, CFUUIDRef) = (void *(*)(CFAllocatorRef, CFUUIDRef))CFBundleGetFunctionPointerForName(pluginBundle, CFSTR("New_iGlasses_PlugIn_Loader"));
    assert(func_ptr != nullptr && "Could not find symbol in the plugin!");
    std::cout << "Successfully tapped into iGlasses yo!" << std::endl;
    return  CMIOPluginTracerGetHookedInterface(func_ptr, allocator, requestedTypeUUID);
  }
}

