#!/usr/bin/python3
import os
import sys
import stat
from subprocess import Popen, PIPE

def mkdir(DIR):
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def rmdir(DIR):
    if os.path.exists(DIR):
        os.rmdir(DIR)

def chmod_x( filename ):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)

def link( src, dst, alias=None ):
    basename = os.path.basename(src) if alias is None else alias
    full_src = os.path.join(os.getcwd(), src)
    os.symlink( full_src, os.path.join( dst, basename ))

def make_executable(filename, python_version="python3"):

    path = is_available(python_version)

    if path is None:
        return False
    
    chmod_x(filename)

    SHEBANG = "#!"+path

    with open(filename, 'r') as original:
        data = original.read()

    if data[:2] != "#!":
        with open(filename, 'w') as modified:
            modified.write( SHEBANG + "\n" + data)
    else:
        print("file already executable: " + data.split('\n')[0])

    return True


def execute(command):
    commands = command.split(" ")
    p = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    output, err = p.communicate( b"input data that is passed to subprocess stdin")
    return (output.decode("utf-8"))


def is_available(python_version):
    output = execute( "which " + python_version )
    path = output.split("\n")[0]
    if "/" in path:
        return path
    return None

def main():

    import argparse

    parser = argparse.ArgumentParser(prog="globalize")
    
    parser.add_argument("--setup", "-s", action="store_true", help="run only once after installing module")

    parser.add_argument("--target", "-t", help="target file that should become a global command (multiple targets possible)", nargs="+")
    parser.add_argument("--pyversion", "-p", help="choose the python version to execute in")
    parser.add_argument("--alias", "-a", help="alias for the program", nargs="+")

    args = parser.parse_args()
    use_py = "python3" if args.pyversion is None else args.pyversion

    HOME = os.getenv("HOME")
    MY_GLOBAL = os.path.join( HOME, "globalpy-bin" )

    mkdir(MY_GLOBAL)

    if args.setup:
        print("PyGlobal will allow you to globalize your python scripts, so that you can run them from anywhere in your console")
        config_path = input("Enter the full path to your config file\n"+
                "most of the times it is something like: \n" +
                "/home/username/.bash_profile\n" +
                "/home/username/.bashrc\n")
        tmp = input("Now we will create a folder in your home directory, where we will store all of the global scripts\n \
                folder name: pyglobal-bin\nPress Enter to proceed")
        mkdir(MY_GLOBAL)
        tmp = input("At last, I will add this directory to your PATH\nPress Enter to proceed")
        
        run = "echo 'export PATH=\""+MY_GLOBAL+":$PATH\"' >> " + config_path
        print(run)
        os.system(run)
        print("congrats! Ready to go :)")
    else:
        if args.target is None:
            print("Must specify either -s or -t")
            sys.exit()
            
        for idx, target in enumerate(args.target):
            make_executable(target, use_py)
            if args.alias is None:
                link( target, MY_GLOBAL )
            else:
                link( target, MY_GLOBAL, args.alias[idx] )

if __name__ == '__main__':
    main()


