# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from .common import Constants

RELATIVE_PATHS = Constants({'src':'src',
                  'include':'include',
                  'experiments':'experiments',
                  'analyses':'analyses',
                  'run_data':'data/runs',
                  'persistent_data':'data/persistent',
                  'saved_data':'data/saved',
                  'xanity_data':'.xanity'
                  })

COMMANDS = Constants({
        'RUN': ['run'],
        'ANAL': ['anal','analyze','analyse','analysis','analyses'],
        'SETUP': ['setup'],
        'INIT': ['init', 'initialize','initialise'],
        })

ACTIONS = Constants({
        'RUN': 'run',
        'ANAL': 'anal',
        'INIT': 'init',
        'SETUP':'setup',
})

ACTIVITIES = Constants({
        'CONST': 'constructing_xanity_object',
        'ORIENT': 'orienting',
        'EXP': 'experimenting',
        'ANAL': 'analyzing',
})

DIRNAMES = Constants({
        'SAVED_VARS':"xanity_variables",
        })