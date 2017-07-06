# version.py
# 2016 Bibhas Acharya <mail@bibhas.com>

VERSION_FILE_PREAMBLE = """# DO NOT, I REPEAT DO NOT, hand edit this file.
# Use the commands ver, ver++ or ver-- to do it instead.

"""

def readVersion(filepath):
    
    f    = open(filepath, 'r')
    
    c = f.read()
    
    f.close()
    
    acc = ""
    
    for line in c.split("\n"):
        
        if not line.startswith("#"):
            
            acc += line
            
    return acc.strip("\n").strip()

def writeVersion(filepath, newVersion):
    
    f = open(filepath, 'w')
    
    f.write(VERSION_FILE_PREAMBLE + newVersion)
    
    f.close()

def incrementVersion(oldVersion):
    
    parsedVersion = [int(x) for x in oldVersion.split(".")]
    
    newVersion = list(parsedVersion)
    
    newVersion[-1] = newVersion[-1] + 1
    
    return ".".join([str(x) for x in newVersion])

def decrementVersion(oldVersion):
    
    parsedVersion = [int(x) for x in oldVersion.split(".")]
    
    newVersion = list(parsedVersion)
    
    newVersion[-1] = newVersion[-1] - 1
    
    return ".".join([str(x) for x in newVersion])