// tracer.mm

#include <iostream>
#include <lldb/API/LLDB.h>
#include <utils/scope_exit_guard.h>
#include <utils/compute.h>

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
      "/bin/ls", "x86_64", NULL, true, error
    );
    assert(error.Success() && "Failed to create target!");
    assert(resp.IsValid() && "Target created but is invalid!");
    return resp;
  });
  // Add breakpoints
  lldb::SBBreakpoint breakpoint = COMPUTE({
    std::cout << "Creating breakpoint..." << std::endl;
    lldb::SBBreakpoint resp = target.BreakpointCreateByName("malloc");
    auto callback = [](void *baton, lldb::SBProcess& process, lldb::SBThread& thread, lldb::SBBreakpointLocation& location) -> bool {
      // Log where we're at
      lldb::SBFrame frame = thread.GetFrameAtIndex(0);
      std::cout << "Now in function named : " << frame.GetFunctionName() << " in process with pid = " << process.GetProcessID() << std::endl;
      // Print the argument
      // x86_64 calling convention : RDI, RSI, RDX, RCX, R8, R9, XMM0–7
      lldb::SBValue rsiValue = frame.FindValue("rdi", lldb::eValueTypeRegister);
      std::cout << "\tRequested size : " << rsiValue.GetValueAsUnsigned() << std::endl;
      // Next, step out
      thread.StepOut();
      // Then log return value
      lldb::SBValue raxValue = frame.FindValue("rax", lldb::eValueTypeRegister);
      std::cout << "\tReturned : " << raxValue.GetValueAsUnsigned() << std::endl;
      return true;
    };
    resp.SetCallback(callback, 0);
    return resp;
  });
  // Launch process
  lldb::SBProcess process = COMPUTE({
    lldb::SBProcess resp = target.LaunchSimple(nullptr, nullptr, "/Users/Bibhas/Desktop");
    assert(resp.IsValid() && "Failed to attach to remote process!");
    return resp;
  });
  // Poll process for state changes
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
