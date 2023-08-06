#!/usr/bin/env python

import sys
from . import common

if not ( sys.argv[0] == '-m' and sys.argv[1] in ['init', 'initialize'] ):
    if 'xanity' not in locals():
        print('parsing xanity project')
        xanity = common.Xanity()

def log(message):
    xanity.log(message)

def save_variable(name, value):
    xanity.save_variable(name, value)

def run_hook():
    xanity.run_all_exps()
    
#def run():
#    # check whether you're in a xanity path
#    inxanity=True if os.path.exists('.xanity') else False
#        
#    # look for .xanity/.runlock
#    xanity_running=True if os.path.exists('.xanity/.runlock') else False
#    
#    if xanity_running:
#        #load metadata
#        with open('.xanity/.runlock','rb') as mdfile:
#            metadata = dill.load(mdfile)
#        pass
#            
#    else:
#        sys.path.append('.xanity')
#        import run_experiments
#        run_experiments(__name__)
