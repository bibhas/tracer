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

static inline std::string reasonToString(lldb::StopReason reason) {
  switch (reason) {
    case lldb::eStopReasonNone : { return "eStopReasonNone"; }
    case lldb::eStopReasonTrace : { return "eStopReasonTrace"; }
    case lldb::eStopReasonBreakpoint : { return "eStopReasonBreakpoint"; }
    case lldb::eStopReasonWatchpoint : { return "eStopReasonWatchpoint"; }
    case lldb::eStopReasonSignal : { return "eStopReasonSignal"; }
    case lldb::eStopReasonException : { return "eStopReasonException"; }
    case lldb::eStopReasonExec : { return "eStopReasonExec"; }
    case lldb::eStopReasonPlanComplete : { return "eStopReasonPlanComplete"; }
    case lldb::eStopReasonThreadExiting : { return "eStopReasonThreadExiting"; }
    case lldb::eStopReasonInstrumentation : { return "eStopReasonInstrumentation"; }
    case lldb::eStopReasonInvalid : { return "eStopReasonInvalid"; }
  }
  return "n/a";
}

static inline std::string stateToString(lldb::StateType state) {
  switch (state) {
    case lldb::eStateInvalid : { return "eStateInvalid"; }
    case lldb::eStateUnloaded : { return "eStateUnloaded"; }
    case lldb::eStateConnected : { return "eStateConnected"; }
    case lldb::eStateAttaching : { return "eStateAttaching"; }
    case lldb::eStateLaunching : { return "eStateLaunching"; }
    case lldb::eStateStopped : { return "eStateStopped"; }
    case lldb::eStateRunning : { return "eStateRunning"; }
    case lldb::eStateStepping : { return "eStateStepping"; }
    case lldb::eStateCrashed : { return "eStateCrashed"; }
    case lldb::eStateDetached : { return "eStateDetached"; }
    case lldb::eStateExited : { return "eStateExited"; }
    case lldb::eStateSuspended : { return "eStateSuspended"; }
  }
  return "n/a";
}

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
    lldb::SBBreakpoint resp = target.BreakpointCreateByName("CMIOObjectHasProperty");
    auto callback = [](void *baton, lldb::SBProcess& process, lldb::SBThread& thread, lldb::SBBreakpointLocation& location) -> bool {
      lldb::SBAddress address = location.GetAddress();
      std::cout << address.GetFileAddress() << ", " << thread.GetIndexID() << ", " << mach_absolute_time() << std::endl;
      lldb::SBFrame frame = thread.GetFrameAtIndex(0);
      std::cout << "Now in function named : " << frame.GetFunctionName() << " in process with pid = " << process.GetProcessID() << std::endl;
      // x86_64 calling convention : RDI, RSI, RDX, RCX, R8, R9, XMM0–7
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
      std::cout << readAddress.mSelector << std::endl;
      std::cout << IntToFourCharString(readAddress.mSelector) << std::endl;
      // Next, step out
      thread.StepOut();
      usleep(1000);
      // Then get stop return value
      lldb::SBThread newThread = process.GetSelectedThread();
      lldb::SBFrame newFrame = newThread.GetFrameAtIndex(0);
      lldb::SBValue raxValue = newFrame.FindValue("rax", lldb::eValueTypeRegister);
      uint64_t boolValue = raxValue.GetValueAsUnsigned();
      std::cout << "\tReturned " << boolValue << std::endl;
      return true;
    };
    resp.SetCallback(callback, 0);
    return resp;
  });
  // Start process
  lldb::SBProcess process = COMPUTE({
    lldb::SBError error;
    lldb::SBListener mockListener;
    lldb::SBProcess resp = target.AttachToProcessWithName(mockListener, "avconferenced", false, error);
    assert(error.Success() && "Failed to attach to remote process!");
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
