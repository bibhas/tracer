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
  lldb::SBBreakpoint breakpoint = COMPUTE({
    std::cout << "Creating breakpoint..." << std::endl;
    lldb::SBBreakpoint resp = target.BreakpointCreateByName("CMIOObjectGetPropertyData");
    auto callback = [](void *baton, lldb::SBProcess& process, lldb::SBThread& thread, lldb::SBBreakpointLocation& location) -> bool {
      lldb::SBFrame frame = thread.GetFrameAtIndex(0);
      std::cout << "Now inside : " << frame.GetFunctionName() << " (in process with pid = " << process.GetProcessID() << ")" << std::endl;
      // x86_64 calling convention : RDI, RSI, RDX, RCX, R8, R9, XMM0–7
      lldb::SBValue rdiValue = frame.FindValue("rdi", lldb::eValueTypeRegister);
      lldb::SBValue rsiValue = frame.FindValue("rsi", lldb::eValueTypeRegister);
      uint64_t ptrAddress = rsiValue.GetValueAsUnsigned();
      lldb::SBError readError;
      CMIOObjectPropertyAddress readAddress;
      size_t toReadSize = sizeof(CMIOObjectPropertyAddress);
      process.ReadMemory(ptrAddress, &readAddress, toReadSize, readError);
      if (readError.Fail()) {
        std::cout << "Error Message : " << readError.GetCString() << std::endl;
        exit(-1);
      }
      std::cout << "FOR OBJECTID = " << rdiValue.GetValueAsUnsigned() << std::endl;
      std::cout << "\tGot property selector = " << tryTranslateSelectorName(readAddress.mSelector) << " (" << IntToFourCharString(readAddress.mSelector) << ")" << std::endl;
      std::cout << "\tGot scope = " << tryTranslateScopeName(readAddress.mScope) << std::endl;
      std::cout << "\tGot element = " << tryTranslateElementName(readAddress.mElement) << std::endl;
      // Next, step out
      thread.StepOut();
      // Then get stop return value
      lldb::SBValue returnValue = thread.GetStopReturnValue();
      uint64_t boolValue = returnValue.GetValueAsUnsigned();
      std::cout << "\tReturned " << boolValue << std::endl;
      lldb::SBFrame newFrame = thread.GetFrameAtIndex(0);
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