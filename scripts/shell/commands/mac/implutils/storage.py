# storage.py
# 2016 Bibhas Acharya <mail@bibhas.com>

import os, sys, cPickle

class Storage:
    
    """ A simple storage system that reads/writes 
        from/to Storage.kBackingStorePath. Useful for 
        saving persistent data.
    """
    
    kBackingStorePath = os.path.abspath(
        
        os.path.expanduser("~/.r59build.rc")
    )
    
    @staticmethod
    def set(key, value):
        
        f = open(Storage.kBackingStorePath, "r")
        
        if f == None:
            
            return False
        
        c = f.read()
        
        f.close()
        
        d = {}
        
        if c != "":
            
            d = cPickle.loads(c)
        
        d[key] = value
        
        f = open(Storage.kBackingStorePath, "w")
        
        if f == None:
            
            return False
        
        f.truncate(0)
        
        f.write(cPickle.dumps(d))
        
        f.close()
        
        return True
    
    @staticmethod
    def get(key):
        
        if not os.path.exists(Storage.kBackingStorePath):
            
            open(Storage.kBackingStorePath, "w").close()
        
        f = open(Storage.kBackingStorePath, "r")
        
        d = {}
        
        c = f.read()
        
        if c != "":
            
            d = cPickle.loads(c)
        
        f.close()
        
        v = None
        
        if d.has_key(key):
            
            v = d[key]
        
        return v
