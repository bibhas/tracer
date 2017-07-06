# linetail.py
# 2016 Bibhas Acharya <mail@bibhas.com>

import os, sys
import subprocess
import threading
import re, sys
import signal
import tempfile
import log

DEVNULL = open(os.devnull,"w")

TEMPNAME = os.path.join(tempfile.mkdtemp(), "linetail_stderr")

def cleanup(move_line_up=False):

    sys.stdout.write("\033[?25h")
    
    sys.stdout.flush()
    
    if move_line_up == True:
        
        sys.stdout.write("\r")
        
        sys.stdout.write("\033[K")
        
        sys.stdout.write("\033[1A")
        
        sys.stdout.write("\r")
        
        sys.stdout.write("\033[K")
        
        sys.stdout.flush()
        
    else:
        
        sys.stdout.write("\r")
        
        sys.stdout.write("\033[K")
        
        sys.stdout.flush();

def linetail(filter_func, maxchars, move_line_up, program, arguments=[]):

    def thread_func(filter_func, program, arguments=[]):
      
        stderr_f = open(TEMPNAME, "w")

        stderr_f.seek(0)

        try:
          
            proc=subprocess.Popen(
                
                [program] + arguments,

                stdout=subprocess.PIPE,
                
                stderr=stderr_f
            )
            
        except:
            
            print("Error in executing subprocess!")
            
            return False
            
        def process_line(line):
            
            if line != "":
                
                line = line.replace("\n", "")
                
                line = line.strip(" ")
                
                out = filter_func(line)[0:maxchars]
                
                if out != None or out.strip(" ") != "":
                    
                    stderr_f.writelines(out + "\n")

                    stderr_f.flush()
                    
                    sys.stdout.write("\033[K")
                    
                    sys.stdout.write("\r" + out[0:maxchars])
                    
                    sys.stdout.flush();
                    
        while proc.poll() is None:
            
            out = iter(proc.stdout.readline, '')
            
            for line in out:
                
                process_line(line)

        out, err = proc.communicate()
        
        for line in out.split("\n"):
            
            process_line(line)
        
        cleanup(False)

        if proc.returncode != 0:
            
            stderr_f.close()

            stderr_f = open(TEMPNAME, "r")

            stderr_f.seek(0)
            
            c = stderr_f.read()

            c = "\n" + c.strip("\n") + "\n"
            
            for line in c.split("\n"):

                log.color_log_inc("|  ", "RED")
                
                sys.stdout.flush()

                sys.stdout.write(line + "\n")

            os._exit(proc.returncode)
            
        return True
    
    sys.stdout.write("\033[?25l")
    
    sys.stdout.flush()
    
    try:
        
        t = threading.Thread(target=thread_func, args=[filter_func, program, arguments])
        
        t.start()
        
        t.join()
        
    except:
        
        pass
       
    cleanup(move_line_up)
