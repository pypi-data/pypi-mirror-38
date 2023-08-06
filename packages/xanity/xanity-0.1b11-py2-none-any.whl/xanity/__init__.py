#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from .Xanity import Xanity

fns_to_expose = [
        'run_hook',
        'experiment_parameters',
        'associated_experiments',
        'log',
        'save_variable',
        'load_variable',
        'analyze_this',
]

vars_to_expose = [
        'status',
        ]

thismodule = sys.modules[__name__]

if 'xanity' not in locals():
    
    # define placeholder attrs
    for fn in fns_to_expose:
        setattr(thismodule, fn, lambda: None)
    for var in vars_to_expose:
        setattr(thismodule, var, None)
    
    # create xanity object
    xanity = Xanity()
    
    # go through and redefine attrs using the real things
    for fn in fns_to_expose:
        setattr(thismodule, fn, getattr(xanity, fn))
    for var in vars_to_expose:
        setattr(thismodule, var, getattr(xanity, var))

    # do the real initialization
    xanity._orient()
