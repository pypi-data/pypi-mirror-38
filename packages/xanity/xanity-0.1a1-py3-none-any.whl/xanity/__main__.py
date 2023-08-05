#!/usr/bin/env python

import sys
import argparse

def main():
  parser = argparse.ArgumentParser(description='Manage scientific experiments, parameters, and analyses')
  parser.add_argument('action', type=str, help='action for xanity to do')
  args, remaining_args = parser.parse_known_args()
  remaining_args = ' '.join(remaining_args)
  
  #print('args: {}   rem_args:{}'.format(args,remaining_args))
  #print('args.action: {}'.format(args.action))
  
  if args.action == 'init' or args.action == 'initialize':
    from . import initialize
    sys.exit(initialize.main(remaining_args))
  
  elif args.action == 'setup':
    from . import setup
    sys.exit(setup.main(remaining_args))
    
  elif args.action == 'run':
    from . import run
    sys.exit(run.main(remaining_args))
    
  elif args.action == 'analyse' or args.action == 'analyze' or args.action == 'anal':
    from . import analyze
    sys.exit(analyze.main(remaining_args))
  
  else:
    print('did not find action')
    sys.exit(1)
    
if __name__=="__main__:
  sys.exit(main())
  