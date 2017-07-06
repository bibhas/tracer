# programs.py 
# 2016 Bibhas Acharya <mail@bibhas.com> 

import os, subprocess, platform 
import traceback 
import log 

wd = os.getcwd() 

def ensure_programs_availability(exit_on_failure, programs): 
    
    should_exit = False 
    
    for p in programs.keys(): 
        
        if subprocess.call("type " + p, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 1: 
            
            log.color_log("Could not find %s. %s" % (p, programs[p]), "RED") 
            
            should_exit = True 
            
    if should_exit and exit_on_failure: 
        
        exit(-1) 

def cd(path, should_log=True): 
    
    if should_log: 
        
        _p = os.path.relpath(path, wd) 
        
        log.color_log("Changing working directory to %s" % _p, "GRAY") 
        
    os.chdir(path) 

def ln(src, dest, symbolic=True, should_log=True): 
    
    if should_log: 
        
        _src_p = os.path.relpath(src, wd) 
        
        _dest_p = os.path.relpath(dest, wd) 
        
        if symbolic: 
            
            log.color_log("Soft linking %s to %s" % (_src_p, _dest_p), "GRAY") 
            
        else: 
            
            log.color_log("Hard linking %s to %s" % (_src_p, _dest_p), "GRAY") 
            
    cmd = "ln -f -s %s %s" if symbolic else "ln -f %s %s" 
    
    status = os.system(cmd % (src, dest)) 
    
    if status is not 0: 
        
        exit(status) 

def ls(path, should_log=True): 
    
    if should_log: 
        
        _p = os.path.relpath(path, wd) 
        
        log.color_log("Listing contents of %s" % _p, "GRAY") 
        
    # list contents of the given path to stdout 
    
    status = os.system("ls %s" % path) 
    
    if status is not 0: 
        
        exit(status) 

def mv(src, dest, flags="", should_log=True): 
    
    if should_log: 
        
        _s = os.path.relpath(src, wd) 
        
        _d = os.path.relpath(dest, wd) 
        
        if flags != "": 
            
            log.color_log("Moving item '%s' to %s with flags '%s'" % (_s, _d, flags), "GRAY") 
            
        else: 
            
            log.color_log("Moving item '%s' to %s" % (_s, _d), "GRAY") 
            
    status = os.system("mv %s %s %s" % (flags, src, dest)) 
    
    if status is not 0: 
        
        exit(status) 

def cp(src, dest, flags="", should_log=True): 
    
    if should_log: 
        
        _s = src 
        
        _s = os.path.relpath(_s, wd) 
        
        _d = os.path.relpath(dest, wd) 
        
        if flags != "": 
            
            log.color_log("Copying item '%s' to %s with flags '%s'" % (_s, _d, flags), "GRAY") 
            
        else: 
            
            log.color_log("Copying item '%s' to %s" % (_s, _d), "GRAY") 
            
    status = os.system("cp %s \"%s\" \"%s\"" % (flags, src, dest)) 
    
    if status is not 0: 
        
        exit(status) 

def rm(src, flags="", should_log=True, silent=False): 
    
    if should_log: 
        
        _s = src 
        
        _s = os.path.relpath(_s, wd) 
        
        if flags != "": 
            
            log.color_log("Removing items '%s' with flags '%s'" % (_s, flags), "GRAY") 
            
        else: 
            
            log.color_log("Removing items '%s'" % _s, "GRAY") 
            
    cmd = ["rm", flags, src] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
      if silent == False: 
          
        print err 
        
        exit(-1) 


def mkdir(path, should_log=True): 
    
    _p = os.path.relpath(path, wd) 
    
    if should_log: 
        
        log.color_log("Making directory at %s" % _p, "GRAY") 
        
    s = os.system("mkdir %s" % path) 

def mkdirs(path, should_log=True): 
    
    _p = os.path.relpath(path, wd) 
    
    if should_log: 
        
        log.color_log("Recursively making directories at %s" % _p, "GRAY") 
        
    s = os.system("mkdir -p %s" % path) 

def chk(path, make_exist=True): 
    
    if not os.path.exists(path): 
        
        mkdirs("'%s'" % path, should_log=True) 

def gyp(path, format="ninja", location=".", defines={}, should_log=True): 
    
    if should_log: 
        
        _p = os.path.relpath(path, wd) 
        
        log.color_log("Generating %s files from %s" % (format, _p), "GRAY") 
        
    d_str = "" 
    
    for key in defines.keys(): 
        
        d_str += "-D%s=%s " % (key, defines[key]) 
        
    plat = platform.machine() 
    
    cmd = "gyp -f %s -D target_arch=\"%s\" --depth=. -D GYP_GENERATOR_NAME=%s %s --generator-output=%s '%s'" % (format, plat, format, d_str.rstrip(), location, path) 
    
    status = os.system(cmd) 
    
    if status != 0: 
        
        log.color_log("GYP failed to execute successfully...", "RED") 
        
        exit(-1) 

def ninja(target=None, clean=False, should_log=True): 
    
    status = 0 
    
    if clean: 
        
        if should_log: 
            
            _p = os.path.relpath(os.getcwd(), wd) 
            
            log.color_log("Cleaning ninja build files at %s" % _p, "GRAY") 
            
        if target == None: 
            
            status = os.system("ninja -t clean") 
            
        else: 
            
            status = os.system("ninja -t clean %s" % target) 
            
    else: 
        
        if should_log: 
            
            _p = os.path.relpath(os.getcwd(), wd) 
            
            log.color_log("Building targets declared in %s" % _p, "GRAY") 
            
        if target == None:     
            
            status = os.system("ninja") 
            
        else: 
            
            status = os.system("ninja %s" % target) 
            
    if status != 0: 
        
        log.color_log("Ninja failed to build successfully...", "RED") 
        
        exit(-1) 

def ssh(username, ipaddress, port=22, action=None, should_log=False): 
    
    if should_log: 
        
        log.color_log("Connecting to %s:%s as %s..." % (ipaddress, port, username)) 
        
    cmd = "ssh \'%s\'@%s -p %s" % (username, ipaddress, port) 
    
    if action != None: 
        
        cmd += " -t \"%s\"" % action 
        
    status = os.system(cmd) 
    
    if status != 0: 
        
        log.color_log("Failed to SSH successfully...", "RED") 

def strip(path, should_log=True): 
    
    if (path == None) or (os.path.exists(path) == False): 
        
        log.color_log("Strip failed; please provide valid path.", "RED") 
        
        exit(-1) 
        
    if should_log: 
        
        log.color_log("Stripping symbols from %s" % path.split("/")[0], "GRAY") 
        
    cmd = ["strip", "-x", path] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        if "changes being made to the file will" in err: 
            
            log.color_log("Strip failed because %s is already codesigned. Rebuild and try again!" % path.split("/")[0], "RED") 
            
            exit(-1) 
            
        else: 
            
            print(err) 
            
            log.color_log("Strip failed to complete successfully...", "RED") 
            
            exit(-1) 

def dsymutl(src, dest, should_log=True): 
    
    if (src == None) or (os.path.exists(src) == False): 
        
        log.color_log("DSYM generation (dsymutil) failed; please provide a valid source file.", "RED") 
        
        exit(-1) 
        
    if os.path.exists(dest): 
        
        rm(dest, should_log=False, silent=True) 
        
    cmd = ["dsymutil", src, dest] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    print "---" 
    
    if err != "": 
        
        print err 
        
    print output 

def codesign(author=None, entitlements=None, target=None, flags=[], should_log=True): 
    
    status = 0 
    
    if author is None: 
        
        log.color_log("Codesign failed; please provide author name.", "RED") 
        
        exit(-1) 
        
    if target is None: 
        
        log.color_log("Codesign failed; please provide a valid target", "RED") 
        
        exit(-1) 
        
    if should_log: 
        
        log.color_log("Code signing %s" % target, "GRAY") 
        
    cmd = [] 
    
    if entitlements is None: 
        
        cmd = ["codesign", "--timestamp=none", "-s", "%s" % author, "%s" % target] 
        
    else: 
        
        cmd = ["codesign", "--timestamp=none", "-s", "%s" % author, "--entitlements", entitlements, "%s" % target] 
        
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        if "is already signed" in err: 
            
            log.color_log("Codesigning failed because %s is already codesigned. Rebuild and try again!" % target, "RED") 
            
            exit(-1) 
            
        elif "replacing existing signature" in err: 
            
            pass 
            
        else: 
            
            print(err) 
            
            log.color_log("Codesigning failed to complete successfully...", "RED") 
            
            exit(-1) 

def pkgbuild(reference=".", tempdir=".", project=None, should_log=True): 
    
    if project == None: 
        
        raise Exception("Package building failed; please provide a .pkgproj file to use.") 
        
    if should_log: 
        
        log.color_log("Package building %s" % project.split("/")[-1], "GRAY") 
        
    cmd = ["packagesbuild", "-F", reference, "-t", tempdir, project] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if output.find("Build Successful") == -1 or err != "":
    
        print output, err
        
        log.color_log("Package building failed to complete successfully...", "RED") 
        
        exit(-1) 

def pkginstall(path=None, target="/", should_log=True): 
    
    if path == None: 
        
        raise Exception("Installation failed; please provide a .pkg file to use.") 
        
    if should_log: 
        
        log.color_log("Installing %s" % path.split("/")[-1], "GRAY") 
        
    cmd = ["sudo", "installer", "-pkg", path, "-target", target] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        print(err) 
        
        log.color_log("Installation failed to complete successfully...", "RED") 
        
        exit(-1) 
        
    else: 
        
        log.color_log("\n".join(output.split("\n")[0:-1]), "GRAY") 

def rsync(dest, remoteuser, remoteaddr, remotesrc, remoteexcludes, should_log=True): 
    
    remoteip, remoteport = remoteaddr.split(":") 
    
    if should_log: 
        
        log.color_log("Rsyncing %s::%s with %s..." % (remoteip, remotesrc, dest), "GRAY")     
        
    exstr = " ".join([("--exclude=**/%s" % x) for x in remoteexcludes]) 
    
    cmdstr = "rsync -e 'ssh -p %s' -zuPra %s %s@%s:%s %s" % (remoteport, exstr, remoteuser, remoteip, remotesrc, dest) 
    
    status = os.system(cmdstr) 
    
    if status != 0: 
        
        log.color_log("Rsync failed to execute successfully...", "RED") 
        
        exit(-1) 

def productbuild(target, plist, author, dest, should_log=True): 
    
    if should_log: 
        
        log.color_log("Packaging %s" % target, "GRAY") 
        
    cmd = ["productbuild", "--component", target, "/Applications", "--sign", author, "--product", plist, dest] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        print(err) 
        
        log.color_log("productbuild failed to complete successfully...", "RED") 
        
        exit(-1) 

def productsign(path, author, should_log=True): 
    
    if should_log: 
        
        log.color_log("Signing %s" % path, "GRAY") 
        
    dest = path + "_2" 
    
    cmd = ["productsign", "--sign", "%s" % author, path, dest] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        print(err) 
        
        log.color_log("productbuild failed to complete successfully...", "RED") 
        
        exit(-1) 
        
    else: 
        
        os.remove(path) 
        
        os.rename(dest, path) 

def zip(path, dest, should_log=True): 
    
    if should_log: 
        
        log.color_log("Zipping %s to %s" % (path, dest), "GRAY") 
        
    cmd = None 
    
    if type(path) == list: 
        
      cmd = ["zip", "-vr", dest] + path 
      
    else: 
        
      cmd = ["ditto", "-c", "-k", "--keepParent", "--rsrc", path, dest] 
      
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        print(err) 
        
        log.color_log("Zip failed to complete successfully...", "RED") 
        
        exit(-1) 

def dropdmg(path, layout_folder, should_log=True): 
    
    if should_log: 
        
        log.color_log("Generating DMG from %s" % path, "GRAY") 
        
    cmd = ["dropdmg", "--append-version-number", "--internet-enabled", "--layout-folder=%s" % layout_folder, path] 
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    output, err = proc.communicate() 
    
    if err != "": 
        
        print(err) 
        
        log.color_log("DMG creation failed to complete successfully...", "RED") 
        
        exit(-1)
