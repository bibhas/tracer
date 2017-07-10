// tracer.mm
// 2017 Bibhas Acharya <mail@bibhas.com>

#include <iostream>
#include <lldb/API/LLDB.h>
#include <mach/mach.h>
#include <mach/mach_time.h>
#include <CoreMediaIO/CMIOHardwareObject.h>
#include <utils/scope_exit_guard.h>
#include <utils/fourchar.h>
#include <utils/compute.h>
#include "CMIOTypes.h"

static inline lldb::SBBreakpoint getCreateBreakpointForFunctionWithName(lldb::SBTarget& target, const std::string& funcName) {
  return target.BreakpointCreateByName(funcName.c_str());
}

static inline lldb::SBBreakpoint getCreateBreakpointForAddressAtModule(lldb::SBTarget& target, lldb::addr_t address, const std::string& moduleName) {
  lldb::SBModule cmioModule = COMPUTE({
    for (int i = 0; i < target.GetNumModules(); i++) {
      lldb::SBModule module = target.GetModuleAtIndex(i);
      lldb::SBFileSpec fileSpec = module.GetFileSpec();
      if (std::string(fileSpec.GetFilename()) == moduleName) {
        return module;
      }
    }
    assert(false && "Could not find requested module in module list!!");
  });
  // Address to breakpoint in CoreMediaIO.framework ko address 0x31415
  lldb::SBAddress breakpointAddress = cmioModule.ResolveFileAddress(address);
  return target.BreakpointCreateBySBAddress(breakpointAddress);
}

struct PropertyDataCache {
  uint64_t objectID;
  uint64_t addressPtrAddress;
  uint64_t dataUsedPtrAddress;
  uint64_t dataPtrAddress;
} cachedPropertyData;

int main(int argc, const char **argv) {
  // Setup debugger environment
  lldb::SBDebugger::Initialize();
  scope_exit_guard_t guard([&] {
    std::cout << "Terminating debugger..." << std::endl;
    lldb::SBDebugger::Terminate();
  });
  // Create debugger
  lldb::SBDebugger debugger = COMPUTE({
    std::cout << "Creating debugger..." << std::endl;
    lldb::SBDebugger resp = lldb::SBDebugger::Create();
    assert(resp.IsValid() && "Could not create a valid debugger!");
    resp.SetAsync(false);
    return resp;
  });
  // Create target
  lldb::SBTarget target = COMPUTE({
    std::cout << "Creating target..." << std::endl;
    lldb::SBError error;
    lldb::SBTarget resp = debugger.CreateTarget(
      "/usr/libexec/avconferenced", "x86_64", NULL, true, error
    );
    assert(error.Success() && "Failed to create target!");
    assert(resp.IsValid() && "Target created but is invalid!");
    return resp;
  });
  // Add breakpoints
  lldb::SBBreakpoint preBreakpoint = COMPUTE({
    std::cout << "Creating pre breakpoint..." << std::endl;
    // Address to breakpoint in CoreMediaIO.framework ko address 0x31415
    lldb::SBBreakpoint resp = getCreateBreakpointForFunctionWithName(target, "CMIOObjectGetPropertyData");
    auto callback = [](void *baton, lldb::SBProcess& process, lldb::SBThread& thread, lldb::SBBreakpointLocation& location) -> bool {
      lldb::SBFrame frame = thread.GetSelectedFrame();
      std::cout << "Pre breakpointing at : " << frame.GetFunctionName() << " (in process with pid = " << process.GetProcessID() << ")" << std::endl;
      // x86_64 calling convention : RDI, RSI, RDX, RCX, R8, R9, XMM0–7
      cachedPropertyData.objectID = frame.FindValue("rdi", lldb::eValueTypeRegister).GetValueAsUnsigned();
      cachedPropertyData.addressPtrAddress = frame.FindValue("rsi", lldb::eValueTypeRegister).GetValueAsUnsigned();
      cachedPropertyData.dataUsedPtrAddress = frame.FindValue("r9", lldb::eValueTypeRegister).GetValueAsUnsigned();
      cachedPropertyData.dataPtrAddress = frame.FindValue("xmm0", lldb::eValueTypeRegister).GetValueAsUnsigned();
      lldb::SBError readError;
      CMIOObjectPropertyAddress readAddress;
      size_t toReadSize = sizeof(CMIOObjectPropertyAddress);
      process.ReadMemory(cachedPropertyData.addressPtrAddress, &readAddress, toReadSize, readError);
      if (readError.Fail()) {
        std::cout << "Error Message : " << readError.GetCString() << std::endl;
        exit(-1);
      }
      std::cout << "ID = " << cachedPropertyData.objectID << " "; 
      std::cout << "SEL = " << tryTranslateSelectorName(readAddress.mSelector) << " ";
      std::cout << "SCOPE = " << tryTranslateScopeName(readAddress.mScope) << " "; 
      std::cout << "ELEM = " << tryTranslateElementName(readAddress.mElement) << std::endl;
      return true;
    };
    resp.SetCallback(callback, 0);
    return resp;
  });
  lldb::SBBreakpoint postBreakpoint = COMPUTE({
    std::cout << "Creating post breakpoint..." << std::endl;
    // Address to breakpoint in CoreMediaIO.framework ko address 0x31415
    lldb::SBBreakpoint resp = getCreateBreakpointForAddressAtModule(target, 0x31a94, "CoreMediaIO");
    auto callback = [](void *baton, lldb::SBProcess& process, lldb::SBThread& thread, lldb::SBBreakpointLocation& location) -> bool {
      lldb::SBFrame frame = thread.GetSelectedFrame();
      std::cout << "Post breakpointing at : " << frame.GetFunctionName() << " (in process with pid = " << process.GetProcessID() << ")" << std::endl;
      // x86_64 calling convention : RDI, RSI, RDX, RCX, R8, R9, XMM0–7
      lldb::SBError readError;
      CMIOObjectPropertyAddress readAddress;
      size_t toReadSize = sizeof(CMIOObjectPropertyAddress);
      process.ReadMemory(cachedPropertyData.addressPtrAddress, &readAddress, toReadSize, readError);
      if (readError.Fail()) {
        std::cout << "Error Message : " << readError.GetCString() << std::endl;
        exit(-1);
      }
      std::cout << "FOR OBJECTID = " << cachedPropertyData.objectID << std::endl;
      std::cout << "\tGot property selector = " << tryTranslateSelectorName(readAddress.mSelector) << " (" << IntToFourCharString(readAddress.mSelector) << ")" << std::endl;
      std::cout << "\tGot scope = " << tryTranslateScopeName(readAddress.mScope) << std::endl;
      std::cout << "\tGot element = " << tryTranslateElementName(readAddress.mElement) << std::endl;
      // Then read return value
      lldb::SBValue returnValue = frame.FindValue("rax", lldb::eValueTypeRegister);
      std::cout << "\tReturned " << returnValue.GetValueAsUnsigned() << std::endl;
      return true;
    };
    resp.SetCallback(callback, 0);
    return resp;
  });
  // Start process
  lldb::SBProcess process = COMPUTE({
    lldb::SBError error;
    lldb::SBListener listener = debugger.GetListener();
    lldb::SBProcess resp = target.AttachToProcessWithName(listener, "avconferenced", false, error);
    assert(error.Success() && "Could not attach to avconferenced process");
    assert(resp.IsValid() && "Attached to avconferenced but the process is not valid!!");
    return resp;
  });
  while (1) {
    lldb::StateType state = process.GetState();
    if (state == lldb::eStateStopped) {
      process.Continue();
      std::cout << "----------------" << std::endl;
    }
    else if (state == lldb::eStateExited) {
      std::cerr << "Program exited!" << std::endl;
      break;
    }
  }
  // We're done
  std::cout << "Done." << std::endl;
  return 0; 
}
