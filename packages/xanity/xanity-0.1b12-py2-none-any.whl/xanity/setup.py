#!/usr/bin/env python

import argparse
import os
import subprocess
import pkg_resources
from . import xanity

helptext =  '''
setup an existing xanity directory tree

usage:  xanity setup [help]

xanity setup assumes you're in a xanity tree

\'help\' will print this help message
'''

def main(arg_list=None):
    """ must be called from inside a xanity tree """
    
    parser = argparse.ArgumentParser(
            description='setup an existing xanity project')
    parser.add_argument(
            'help', type=str, nargs='?',
            help=helptext)
    
    arg_list = ' '.join(arg_list) if len(arg_list)>1 else arg_list
    args = parser.parse_args(arg_list) if arg_list else parser.parse_args()
    
    if args.help:
        if args.help == 'help':
            print(helptext)
            return 0
        else:
            print('unrecognized command')
            print(helptext)
            return 1
    
    setup_script = pkg_resources.resource_filename(__name__, 'bin/xanity-setup.sh')
    opwd = os.getcwd()
    os.chdir(xanity.xanity_root)
    #print('stepped inside xanity root')
    subprocess.call(['bash', setup_script, xanity.xanity_root])
    os.chdir(opwd)

if __name__=="__main__":
    main()