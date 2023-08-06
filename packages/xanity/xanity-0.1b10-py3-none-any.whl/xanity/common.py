#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import inspect
import os.path as path

class Experiment(object):
    def __init__(self, name, module):
        self.name = name
        self.module = module
        self.default_params = None
        self.param_dict = None
        self.paramsets = None
        self.exp_dir = None
        self.subexp_dirs = None
        self.success = False
        self.analyses = {}
        
    def update(self, dict_of_values):
        for key,val in dict_of_values.items():
            assert hasattr(self,key), '\'{}\' is not an Experiment parameter'.format(key)
            setattr(self, key, val)
            
class Analysis(object):
    def __init__(self, name, module):
        self.name = name
        self.module = module
        self.experiments = {}
        self.success = False
        
class Status(object):
    def __init__(self):
        self.activity=None
        self.focus=None
        self.sub_index=None
        self.data_dir=None
        self.parameters=None
        self.tripping=None

class Constants(object):
    def __init__(self, dict_of_vals):
        for key,val in dict_of_vals.items():
            setattr(self,key,val)

def _get_live_module_object(module_path):
    spec = importlib.util.spec_from_file_location(path.split(module_path)[-1].split('.py')[0], location=module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _get_mainfn_sig(modulepath):
    live_module = _get_live_module_object(modulepath)
    sig = inspect.signature(live_module.main)
    del live_module
    return sig

def _get_module_obj(modulepath, obj_name):
    module = _get_live_module_object(modulepath)
    if hasattr(module, obj_name):
        return getattr(module, obj_name)
    else:
        return None
