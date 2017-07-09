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
  lldb::SBBreakpoint breakpoint = target.BreakpointCreateByName("CMIOObjectHasProperty");
  // Setup listener
  lldb::SBListener listener = debugger.GetListener();
  // Start process
  lldb::SBProcess process = COMPUTE({
    lldb::SBError error;
    lldb::SBProcess resp = target.AttachToProcessWithName(listener, "avconferenced", false, error);
    assert(error.Success() && "Failed to attach to remote process!");
    return resp;
  });
  for (;;) {
  }
  // We're done
  std::cout << "Done." << std::endl;
  return 0; 
}
