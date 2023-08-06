#!/usr/bin/env python

import argparse
import os
import subprocess
from xanity import xanity

helptext =  '''
setup an existing xanity directory tree

usage:  xanity setup [help]

xanity setup assumes you're in a xanity tree

\'help\' will print this help message
'''

def main(*args, **kwargs):
    """ must be called from inside a xanity tree """
    
    parser = argparse.ArgumentParser(
            description='setup an existing xanity project')
    parser.add_argument(
            'help', type=str, nargs='?',
            help=helptext)
    
    args = parser.parse_args()
    
    if args.help:
        if args.help == 'help':
            print(helptext)
            return 0
        else:
            print('unrecognized command')
            print(helptext)
            return 1
    
    opwd = os.getcwd()
    os.chdir(xanity.xanity_root)
    #print('stepped inside xanity root')
    subprocess.call(['bash','xanity-setup.sh', xanity.xanity_root])
    os.chdir(opwd)

if __name__=="__main__":
    main()