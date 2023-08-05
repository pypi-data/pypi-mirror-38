#!/usr/bin/env python

import sys
import argparse
import os
import os.path as path
import pkg_resources
import subprocess

def orient(*args, description='', help='', must_exist=True, must_be_xanity=True, **kwargs):
  try:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('directory', type=str, nargs='?',
                        help=help)

    if args:
      args = parser.parse_args(args)
    else:
      args = parser.parse_args()

    if args.directory:
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
    
    if must_exist:
      assert path.exists(xanity_path), 'specified path doesn\'t exist'
    if must_be_xanity:
      assert path.exists(path.join(xanity_path,'.xanity')), 'path is not a xanity root'
      print('found xanity root at {}'.format(xanity_path))
    
    return xanity_path

  except Exception as e:
    print(e)
    sys.exit(1)