# project.py
# 2016 Bibhas Acharya <mail@bibhas.com>

import os
import inspect

def source_relative_path(path):
    """
        Takes a path relative to a source file (where this function is being
        called) and returns an absolute path.
    """
    
    currframe = inspect.currentframe()
    
    callframe = inspect.getouterframes(currframe, 2)
    
    _path = os.path.join(os.path.dirname(os.path.abspath(callframe[1][1])), path)
    
    return os.path.normpath(_path)

ROOT_DIR =          source_relative_path("../../../../..")

SOURCE_DIR =        os.path.join(ROOT_DIR, "src")

BUILD_DIR =         os.path.join(ROOT_DIR, "build")

GYP_DIR =           os.path.join(ROOT_DIR, "gyp")

PRJ_SOURCE_DIR =    SOURCE_DIR

PRJ_GYP_FILE =      os.path.join(GYP_DIR, "main.gyp")

PRJ_BUILD_DIR =     os.path.join(BUILD_DIR, "main", "mac")

PRJ_PRODUCT_DIR =   os.path.join(PRJ_BUILD_DIR, "out/Default")

PRJ_SIGN_DIR =      os.path.join(ROOT_DIR, "sign")
