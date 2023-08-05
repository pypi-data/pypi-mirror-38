#!/usr/bin/env python

import sys
import os
import os.path as path
import argparse
import pkg_resources
import shutil
import subprocess
from .cli_wrapper import orient

def main(*args,**kwargs):
  try:
    xanity_path = orient(*args, must_exist=False, must_be_xanity=False, 
      desription='initialize a new xanity project', help='path to new xanity project', **kwargs)

    #pkg_resources.set_extraction_path(xanity_path)
    skel_root = pkg_resources.resource_filename(__name__, 'skeleton')
    #print('skel_root: {}'.format(skel_root))
    
    #if path.exists(xanity_path):
    #  os.rmdir(xanity_path)

    print('merging xanity skeleton into {}'.format(xanity_path))
    subprocess.call(['rsync','-azhu',skel_root+'/', xanity_path+'/','--exclude=__pycache__'])
    return 0
    
  except Exception as e:
    print(e)
    return 1

if __name__ == "__main__":
  sys.exit(main())
