# log.py
# 2016 Bibhas Acharya <mail@bibhas.com>

import os, sys

colors = {
    
    "GRAY" :    "\033[1;30m%s\033[m",
    
    "RED" :     "\033[1;31m%s\033[m",
    
    "GREEN" :   "\033[1;32m%s\033[m",
    
    "YELLOW" :  "\033[1;33m%s\033[m",
    
    "BLUE" :    "\033[1;34m%s\033[m",
    
    "PINK" :    "\033[1;35m%s\033[m",
    
    "CYAN" :    "\033[1;36m%s\033[m",
    
    "WHITE" :   "\033[1;37m%s\033[m",
    
    "NORMAL" :  "\033[m%s\033[m"
}

def color_log_inc(*args):
    
    cursor = 0
    
    maxcursor = len(args)
    
    while 1:
        
        if maxcursor - cursor >= 2:
            
            msg = args[cursor]
            
            color = args[cursor + 1]
            
            if colors.has_key(color):
                
                msg = colors[color] % msg
            
            sys.stdout.write(msg)
            
            cursor += 2
        
        elif maxcursor - cursor == 1:
            
            msg = args[cursor]
            
            sys.stdout.write(msg)
            
            cursor += 1
        
        else:
            
            sys.stdout.flush()
            
            break

def color_log(*args):

    color_log_inc(*args)

    color_log_inc("\n", args[-1])

def move_line_up():
    
    sys.stdout.write("\r")
    
    sys.stdout.write("\033[K")
    
    sys.stdout.write("\033[1A")
    
    sys.stdout.write("\r")
    
    sys.stdout.write("\033[K")
    
    sys.stdout.flush()
    
if __name__ == "__main__":
    
    acc = 0
    
    for i in colors.keys():
        
        color_log("%s : %s" % (str(i), str(acc)), i)
        
        acc += 1
        
