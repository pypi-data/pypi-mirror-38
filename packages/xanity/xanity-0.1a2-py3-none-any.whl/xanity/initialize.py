#!/usr/bin/env python

import sys
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

def main(*args,**kwargs):
    """ must be called from inside a xanity tree """
    
    parser = argparse.ArgumentParser(
            description='initialize a new xanity project')
    parser.add_argument(
            'directory', type=str, nargs='?',
            help=helptext)
    
    args = parser.parse_args()

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

    #pkg_resources.set_extraction_path(xanity_path)
    skel_root = pkg_resources.resource_filename(__name__, 'skeleton')
    #print('skel_root: {}'.format(skel_root))
    
    print('merging xanity skeleton into {}'.format(xanity_path))
    subprocess.call(['rsync','-azhu',skel_root+'/', xanity_path+'/','--exclude=__pycache__'])
    

if __name__ == "__main__":
    main()
    sys.exit(0)
