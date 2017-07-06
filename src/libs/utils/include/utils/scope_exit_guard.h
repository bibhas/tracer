// scope_exit_guard.h
// 2017 Bibhas Acharya <mail@bibhas.com>

#pragma once

#include <functional>

struct scope_exit_guard_t {
  using callback_t = std::function<void (void)>;
  scope_exit_guard_t(callback_t func) : m_callback(func) { }
  ~scope_exit_guard_t() { m_callback(); }
private:
  callback_t m_callback;
};

