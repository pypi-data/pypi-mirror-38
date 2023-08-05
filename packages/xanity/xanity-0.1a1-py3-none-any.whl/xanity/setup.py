#!/usr/bin/env python

import sys
import argparse
import os
import os.path as path
import pkg_resources
import subprocess
from .cli_wrapper import orient

def main(*args, **kwargs):
  try:
    xanity_path = orient(*args,**kwargs, description='setup xanity root', help='path to xanity root')

    # setup_script = pkg_resources.resource_filename('xanity', 'bin/xanity-setup.sh')  # moved to installed scripts

    opwd = os.getcwd()
    os.chdir(xanity_path)
    #print('stepped inside xanity root')
    subprocess.call(['xanity-setup.sh',xanity_path])
    os.chdir(opwd)

    return 0

  except Exception as e:
    print(e)
    return 1

if __name__=="__main__":
  sys.exit(main())

print(__name__)
