#!/usr/bin/env python
import os
import os.path as path
import argparse
import pkg_resources
import subprocess

#from .cli_wrapper import orient

helptext =  '''
initialize a new xanity directory tree, or reset an existing tree
(will not overwrite)

usage:  xanity init [path] [help]

if path is provided, xanity tree will be created there
if path is not provided, xanity tree will be created in the pwd

\'help\' will print this help message
'''

def main(arg_list=None):
    """ must be called from inside a xanity tree """
    print(
"""
#####################################
##             xanity              ##
#####################################""")
    clarg_subroutine(arg_list)
    
    skel_root = pkg_resources.resource_filename(__name__, 'skeleton')
        
    print('merging xanity skeleton into {}'.format(xanity_path))
    subprocess.call(['rsync','-azhu',skel_root+os.sep, xanity_path+os.sep,'--exclude=__pycache__'])
    
    opwd =os.getcwd()
    try:
        os.chdir(xanity_path)
        git_subroutine()
        
    finally:
        os.chdir(opwd)


def clarg_subroutine(arg_list):
    global args
    global xanity_path
    
    parser = argparse.ArgumentParser(
            description='initialize a new xanity project')
    parser.add_argument('directory', type=str, nargs='?',
            help=helptext)

    arg_list = ' '.join(arg_list) if arg_list and len(arg_list)>1 else arg_list
    args = parser.parse_args(arg_list) if arg_list else parser.parse_args()

    if args.directory:
        if args.directory == 'help':
            print(helptext)
            return 1

        dirspec = path.expandvars(path.expanduser(args.directory))
        if dirspec.startswith('/'):
            # absolute path given
            xanity_path = path.join(dirspec)
        else:
            # relative path given
            xanity_path = path.join(os.getcwd(),dirspec)
    else:
      # assume that the pwd is the xanity root
      xanity_path = os.getcwd()
    

def git_subroutine():

    print(
"""
#####################################
##               git               ##
#####################################""")

    gi_pak = path.join(xanity_path,'.gitignore-deploy')
    gi_exist = path.join(xanity_path,'.gitignore')
    
    if (path.isfile(gi_exist)):
        print('found existing .gitignore will not clobber it')
        os.remove(gi_pak)
        
#        # check ages
#        gi_pak_age = os.stat(gi_pak).st_mtime
#        gi_exist_age =  os.stat(gi_exist).st_mtime
#    
#        # overwrite existing
#        os.remove(gi_exist)
#            
    else:
        os.rename(gi_pak, gi_exist)
        print('deployed xanity\'s .gitignore')

    # initialize a git repo
    if subprocess.check_output(['bash','-c','type -t git']):
        if not b'not a git repository' in subprocess.check_output(['git','status']):
            # is a git repo already
            if not b'reinitialized existing' in subprocess.check_output(['git','init',xanity_path]):
                subprocess.call(['git','add','-A'])
                subprocess.call(['git','commit','-am','xanity initial commit'])
            else:
                print('made an initial commit to your new repo')
                print('use \'git status\' to see whats up')


if __name__ == "__main__":
    main()
