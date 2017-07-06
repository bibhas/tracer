# updates.py
# 2016 Bibhas Acharya <mail@bibhas.com>

import os, sys, tempfile
from thirdparty import pysftp
from project import *

class UpdatesSFTPContext:
    
    NFS_UPDATES_USERNAME = "mordgold_vm-updates"

    NFS_UPDATES_PRIVATEKEY = os.path.join(PRJ_SIGN_DIR, "nearlyfreespeechnet", "updates", "updates_rsa4096")
    
    def __init__(self):
        
        self.server = None
        
        self.perror = None
        
        self.scratchfile = tempfile.TemporaryFile()
        
        self.connected = False
        
        try:
            
            self.server = pysftp.Connection(
                
                "ssh.phx.nearlyfreespeech.net", 
                
                username = UpdatesSFTPContext.NFS_UPDATES_USERNAME, 
                
                private_key= UpdatesSFTPContext.NFS_UPDATES_PRIVATEKEY
            )
            
            self.connected = True
            
        except pysftp.AuthenticationException:
            
            self.perror = "Incorrect credentials!"
            
            self.connected = False
        
    def createFile(self, path, source=None, content=None):
        
        return self.updateFile(path, source, content)
        
    def readFile(self, path):
        
        try:
            
            self.scratchfile.seek(0)
           
            self.scratchfile.truncate()
            
            self.server.getfo(path, self.scratchfile)
            
            self.scratchfile.seek(0)
            
            return self.scratchfile.read()
            
        except:
            
            return None
        
    def updateFile(self, path, source=None, content=None):
        
        # content gets precedence over source.
        
        if content != None:
           
           # make tempfile
           
           self.scratchfile.seek(0)
           
           self.scratchfile.truncate()
           
           self.scratchfile.write(content)
           
           self.scratchfile.seek(0)
           
           try:
               
               self.server.putfo(self.scratchfile, remotepath=path, confirm=True)
               
               return True
               
           except:
               
               pass
               
        else:
            
            try:
                
                self.server.put(source, remotepath=path, confirm=True, preserve_mtime=False)
                
                return True
                
            except:
                
                pass
                
        return False
    
    def removeFile(self, path):
        
        try:
            
            self.server.remove(path)
            
            return True
            
        except:
            
            return False
    
    def listDirectory(self, path):
        
        pass
        
    def createDirectory(self, path, recursive=False):
        
        pass
    
    def removeDirectory(self, path, recursive=False):
        
        try:
            
            self.server.rmdir(path)
            
            return True
            
        except:
            
            return False