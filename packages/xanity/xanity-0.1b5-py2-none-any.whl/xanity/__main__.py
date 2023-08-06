#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Manage scientific experiments, parameters, and analyses')
parser.add_argument('action', type=str, help='action for xanity to do. ( init[ialize] | setup | run | anal[yze] )')
args, remaining_args = parser.parse_known_args()

# print('args: {}   rem_args:{}'.format(args,remaining_args))
# print('args.action: {}'.format(args.action))

if args.action in ['init', 'initialize']:
    from . import initialize
    initialize.main(remaining_args)
  
elif args.action == 'setup':
    from . import setup
    setup.main(remaining_args)
    
elif args.action == 'run':
    from . import run
    run.main()
      
elif args.action in ['analyse', 'analyze', 'anal']:
    from . import analyze
    analyze.main(remaining_args)
  
else:
    raise NotImplementedError('xanity did not understand that action')
