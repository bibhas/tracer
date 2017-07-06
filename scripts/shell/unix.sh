#!/bin/sh
# 2016 Bibhas Acharya <mail@bibhas.com>

# Define proper environment variable to set the search
# path correctly for the new subshell.

SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )

# Setup custom string literals for the new subshell.

MESSAGE="You have entered a custom shell. Please use \''\033[1;33mexit\033[m'\' to get out of here.$'\n'2016 Bibhas Acharya, all rights reserved.$'\n'"

# Define an alias for bash and run it.

platform=`uname`

if [ "$platform" = 'Darwin' ]; then
    
    alias bash="echo $MESSAGE;export PS1='\033[1;30m[$(uname -s)] \W> \033[m'; bash --rcfile ~/.bash_profile"
    
    PATH=${PATH}:$SCRIPTPATH/commands/mac; 
    
    export PATH

elif [ "$platform" = 'FreeBSD' ]; then
    
    alias bash="echo -e $MESSAGE;export PS1='\033[1;30m[$(uname -s)] \W> \033[m'; bash --rcfile ~/.bash_profile"
    
    PATH=${PATH}:$SCRIPTPATH/commands/freebsd; 
    
    export PATH
fi

bash

