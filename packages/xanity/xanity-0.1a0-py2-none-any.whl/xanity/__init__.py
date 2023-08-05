#!/usr/bin/env python

import dill
import os

def run():
    # check whether you're in a xanity path
    inxanity=True if os.path.exists('.xanity') else False
        
    # look for .xanity/.runlock
    xanity_running=True if os.path.exists('.xanity/.runlock') else False
    
    if xanity_running:
        #load metadata
#        with open('.xanity/.runlock','rb') as mdfile:
#            metadata = dill.load(mdfile)
        pass
            
    else:
        sys.path.append('.xanity')
        import run_experiments
        run_experiments(__name__)