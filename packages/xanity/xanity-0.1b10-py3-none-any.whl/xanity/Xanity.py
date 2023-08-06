#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dill as pickle
import fnmatch
import tarfile
import json
import os
import os.path as path
import logging
import sys
import argparse
import time
import traceback
import cProfile as profile
import datetime
from copy import deepcopy
from inspect import stack as stack

from .common import Status, Constants, Analysis, Experiment
from .common import _get_live_module_object, _get_mainfn_sig
from .constants import COMMANDS, RELATIVE_PATHS, ACTIONS, ACTIVITIES, DIRNAMES

try:
    from pip._internal.operations import freeze
except ImportError:
    from pip.internal.operations import freeze

class Xanity:
    
    def __init__(self, clargs=None):
        self.status = Status()
        self.status.activity = ACTIVITIES.CONST
        self.start_time = time.localtime()
        self.xanity_root = self.resolve_xanity_root()
        self._parse_args(clargs)
        
    def _orient(self):
        self.status.activity = ACTIVITIES.ORIENT
        if self.action in ACTIONS.SETUP + ACTIONS.INIT:
            return
        
        self.name = self.xanity_root.split('/')[-1]
        self.paths = Constants({key: path.join(self.xanity_root, value) for key,value in RELATIVE_PATHS.__dict__.items()})
        self._parse_avail_modules()
        self._resolve_requests()
        
        if self.action == ACTIONS.RUN:
            rundir_sig  = '{}-debug' if self.args.debug else '{}'
            self.exp_data_dir = path.join(self.paths.run_data, rundir_sig.format(time.strftime('%Y-%m-%d-%H%M%S', self.start_time)))
            self._parse_exps()
            
        self._parse_anal_data()

        self.status.activity = 'waiting'
        
    def _parse_args(self, clargs):
        """ parse commandline arguments """
    
        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs='?', type=str,
                            help='acceptible actions include '+str(ACTIONS.RUN+ACTIONS.ANAL+ACTIONS.SETUP+ACTIONS.INIT))
        parser.add_argument('action-objects', nargs='*',
                            help='specify the experiments to run or data-path to analyze')
        parser.add_argument('-a', '--and-analyze', nargs='*',
                            help="""run: requests that data be analyzed upon completion of experiment\n
                                    analyze: provides list of explicit analyses to run""")
        parser.add_argument('--debug', action='store_true',
                            help='run experiment in debugging mode; experiment code may print additional output or behave differently')
        parser.add_argument('--logging', action='store_true',
                            help='request experiment perform additional logging')
        parser.add_argument('--loadcp', action='store_true',
                            help='request experiment look for and load stored checkpoints from src/include/persistent rather than start from scratch')
        parser.add_argument('--savecp', action='store_true',
                            help='request experiment try to save checkpoints to src/include/persistent (will NOT overwrite)')
        parser.add_argument('--profile', action='store_true',
                            help='run cProfile attatched to your experiment')
        
        self.command = ' '.join(sys.argv)
        
        if not clargs:
            self.args, self.unknownargs = parser.parse_known_args()
        else:
            self.args, self.unknownargs = parser.parse_known_args(clargs)
        
        if self.args.action is None and not hasattr(self.args, 'action_objects'):
            # single file probably called as script
            if self.xanity_root is None:
                # not currently in a xanity root
                self.action = ''

            elif self.paths.experiments in self.command:
                self.action = ACTIONS.RUN
                self.args.action_objects = [self.command.split('/')[-1].rstrip('.py')]
                
            elif self.paths.analyses in self.command:
                self.action = ACTIONS.ANAL
                self.args.action_objects = [self.command.split('/')[-1].rstrip('.py')]
            
            else:
                self.action = ''
        
        else:
            """ parse action """
            self.args.action = self.args.action[0] if isinstance(self.args.action, list) else self.args.action
            if self.args.action in COMMANDS.RUN:
                self.action = ACTIONS.RUN
            elif self.args.action in COMMANDS.ANAL:
                self.action = ACTIONS.ANAL
            elif self.args.action in COMMANDS.INIT:
                self.action = ACTIONS.INIT
            elif self.args.action in COMMANDS.SETUP:
                self.action = ACTIONS.SETUP
            else:
                raise NotImplementedError('xanity didnt recognize that action')
    
    def _resolve_requests(self):    
        """ parse requested action_objects and options"""
       
        # first, resolve declared associations
        for anal in self.avail_analyses.values():
            self._trip_hooks(anal, 'associated_experiments')
        
        # if running, define experiments to run
        if self.action == ACTIONS.RUN:
            if hasattr(self.args, 'action_objects'):
                expreqd = self.args.action_objects
                assert all([item in self.avail_experiments for item in expreqd]), 'couldnt find a requested experiment.'
                self.experiments = {item: self.avail_experiments[item] for item in expreqd}
            else:
                self.experiments = self.avail_experiments
                
            if hasattr(self.args, 'and_analyze'):
                if self.args.and_analyze is None:
                    self.analyses = {}
                else:
                    analreqd = self.args.and_analyze
                    assert all ([item in self.avail_analyses for item in analreqd]), 'couldnt find a requested analysis'
                    self.analyses = {item: self.avail_analyses[item] for item in analreqd}
        
        # if analyzing define anals to run
        elif self.action == ACTIONS.ANAL:
            if hasattr(self.args, 'action_objects'):
                anal_datareqd = self.args.action_objects
                assert all([self.resolve_data_path(item) for item in anal_datareqd]), 'couldnt find a requested analysis.'
                self.anal_data_dirs = anal_datareqd
            else:
                self.anal_data_dirs = self.get_recent_run_path()
            
            if hasattr(self.args, 'and_analyze'):
                if self.args.and_analyze is None:
                    self.analyses = self.avail_analyses
                else:
                    analreqd = self.args.and_analyze
                    assert all ([item in self.avail_analyses for item in analreqd]), 'couldnt find a requested analysis'
                    self.analyses = {item: self.avail_analyses[item] for item in analreqd}

        if self.action == ACTIONS.RUN:
            # for those experiments requested, add analyses, if necessary
            for exp in self.experiments.values():
                self._trip_hooks(exp, 'analyze_this')
            
            # remove non-existant experiments from those analyses that were just added
            for anal in self.analyses.values():
                chop=[]
                for exp in anal.experiments.values():
                    if exp.name not in self.experiments.keys():
                        chop.append(exp.name)
                for name in chop:
                    del anal.experiments[name]
        
    def _parse_exps(self):
        """see if any experiments have asked for param-sets """
        
        # first, get all parameter hooks
        for exp in self.experiments.values():
            self._trip_hooks(exp, 'experiment_parameters')
        
        self._resolve_exp_sigs()
        
        for experiment in self.experiments.values():
    
            if experiment.param_dict:
    
                for key, value in experiment.param_dict.items():
                    if type(value) is not list:
                        experiment.param_dict[key] = [value]
        
                # get number of subexperiments
                frozen_names = tuple(experiment.param_dict.keys())
                kwlens = [len(experiment.param_dict[name]) for name in frozen_names]
                indmax = [item - 1 for item in kwlens]
        
                  # compose all parameter sets
                indvec = [[0] * len(kwlens)]
                while True:
                    tvec = list(indvec[-1])
                    if tvec == indmax:
                        break
                    tvec[-1] += 1
                    for place in reversed(range(len(kwlens))):
                        if tvec[place] > indmax[place]:
                            if place == 0:
                                break
                            else:
                                tvec[place - 1] += 1
                                tvec[place] = 0
        
                    indvec.append(tvec)
                    if indvec[-1] == indmax:
                        break
        
                # store all parameter sets
                # create all the subexperiment info
                experiment.update({
                    'exp_dir': path.join(self.exp_data_dir, experiment.name),
                    'subexp_dirs': [path.join(self.exp_data_dir, experiment.name,'{}_{}'.format(experiment.name, i)) for i, _ in enumerate(indvec) ],
                    'success': [False]*len(indvec),
                    'paramsets': [ {frozen_names[i]: experiment.param_dict[frozen_names[i]][choice] for i, choice in enumerate(vect)} for vect in indvec ],
                })
            
            else:
                # create single subexperiment directory
                experiment.update({
                        'exp_dir': path.join(self.exp_data_dir, experiment.name),
                        'subexp_dirs': [path.join(self.exp_data_dir, experiment.name)],
                        'success': [False],
                        'paramsets': [experiment.default_params],
                })

    
    def _parse_anal_data(self):
        """ unsure... """
        if self.action == ACTIONS.RUN:
            pass  # paths should be set

    def _init_logger(self):
        """ setup a logger ... """
        # create logger
        self.logger = logging.getLogger('xanity_logger')
        self.logger.handlers = []
        self.logger.setLevel(logging.DEBUG)
        
        lsh = logging.StreamHandler(sys.stdout)
        lsh.setFormatter(logging.Formatter(self.exp_data_dir.split('/')[-1] + ' %(asctime)s :%(levelname)s: %(message)s'))
        lsh.setLevel(logging.DEBUG)
        self.logger.addHandler(lsh)
        
    def _attach_root_logger_fh(self):
        lfh = logging.FileHandler(filename=path.join(self.exp_data_dir, 'root.log'))
        lfh.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s: %(message)s'))
        lfh.setLevel(logging.DEBUG)
        self.logger.addHandler(lfh)
    
    def _resolve_exp_sigs(self):
        """ see if there are any parameter sets given for the exp """
        for experiment in self.experiments.keys():
            sig = _get_mainfn_sig(path.join(self.paths.experiments, experiment+'.py'))
            self.experiments[experiment].default_params = {parameter.name: parameter.default for parameter in sig.parameters.values()}

    def _parse_avail_modules(self):
        self.avail_experiments = {name: Experiment(name, path) for name, path in self.list_avail_experiments()}
        self.avail_analyses = {name: Analysis(name, path) for name, path in self.list_avail_analyses()}

#    def _resolve_anal_sigs(self):
#        """ see if there are any parameter sets given for the exp """
#        for analysis in self.analyses.keys():
#            sig = _get_mainfn_sig(path.join(self.paths.analyses, analysis+'.py'))
#            self.analyses[analysis]['parameter_sig'] = {parameter.name: parameter.default for parameter in sig.parameters.values()}

    def get_recent_run_path(self):
        cands = []
        for dirs, subdirs, files in os.walk(self.paths.run_data, followlinks=False):
            if any([subdir in self.analyses for subdir in subdirs]):
                cands.append(dirs)
        cands = sorted(set(cands), key=str.lower)
        return cands[-1]
        
    def resolve_data_path(self, pathstring):
        run_matches = fnmatch.filter(os.listdir(self.paths.run_data), pathstring+'*')
        save_matches = fnmatch.filter(os.listdir(self.paths.saved_data), pathstring+'*')
        
        if run_matches or save_matches:
            return run_matches + save_matches
        else:
            raise FileNotFoundError('couldnt resolve requested data-dir for analysis')
    
    def archive_source_tree(self):
    
        if not self.args.debug:
            # make requirements.txt
            reqs = freeze.freeze()
            with open(path.join(self.exp_data_dir, 'requirements.txt'), mode='w') as reqsfile:
                for line in reqs:
                    reqsfile.write(line + '\n')
    
            filterfn = lambda tarinfo: None if fnmatch.fnmatch(tarinfo.name, '*/data/*') or fnmatch.fnmatch(tarinfo.name, '*/data') else tarinfo
            with tarfile.open(path.join(self.exp_data_dir, 'source.tar.gz'), mode='w:gz') as tarball:
                tarball.add(self.xanity_root, arcname=self.name, filter=filterfn)

            ## dump tarballs of source
            #if path.isdir(path.join(data_dir, 'src')):
            #    tarball = tarfile.open(path.join(self.exp_data_dir, 'src.tar.gz'), mode='w:gz')
            #    tarball.add(src_dir, arcname='src')
            #    tarball.close()
    
            ## dump tarballs of libraries
            #if path.isdir(path.join(data_dir, 'lib')):
            #    tarball = tarfile.open(path.join(self.exp_data_dir, 'lib.tar.gz'), mode='w:gz')
            #    tarball.add(xanity_root + '/lib', arcname='lib')
            #    tarball.close()
    
            ## dump tarballs of includes
            #if path.isdir(path.join(data_dir, 'inc')):
            #    tarball = tarfile.open(path.join(self.exp_data_dir, 'include.tar.gz'), mode='w:gz')
            #    tarball.add(xanity_root + '/include', arcname='include')
            #    tarball.close()

    def savemetadata(self):
        assert self.status.activity == ACTIVITIES.EXP
        data = deepcopy(self)
        del data.logger
        with open(path.join(self.exp_data_dir, 'xanity_metadata.dill'), mode='wb') as f:
            json.dump(data, f)
            
    def resolve_xanity_root(self):
        """ set xanity_root """
    
        pwd = os.getcwd()
        path_parts = pwd.split('/')
    
        for i in range(len(path_parts))[::-1]:
            test_path = '/'+path.join(*path_parts[:i+1])
            if path.isdir(path.join(test_path,'.xanity')):
                return test_path
    
        print('not within xanity tree')
        return None

    def run_basic_prelude(self):
        # set global root dirs and do some basic path operations
        os.chdir(self.xanity_root)
    
        # create logger
        self._init_logger()
        
        # print some info
        self.logger.info(
            '\n'
            '################################################################################\n'
            '## \n'
            '## \'run\' called at {} \n'
            '## {}\n'
            '## xanity_root: {} \n'
            '################################################################################\n'
            '\n'.format(
                datetime.datetime.fromtimestamp(time.mktime(self.start_time)).strftime('%Y-%m-%d %H:%M:%S'),
                vars(self.args),
                self.xanity_root)
        )
        
    def run_exp_prelude(self):
        """
            bunch of meta-level setup for subsequent experiments
        """
        # add root logger to write files
        self._attach_root_logger_fh()
        
        # dump a bunch of tarballs
        self.archive_source_tree()
    
        # print number of subexperiments found:
        for exp in self.experiments.keys():
            if len(self.experiments[exp].paramsets) > 1:
                self.logger.info(
                    '\n'
                    '################################################################################\n'
                    '##  experiment: {} has {} subexperiments:\n'.format(exp, len(self.experiments[exp].paramsets))
                    +'\n'.join(['##     exp #{}: {}'.format(i,param) for i,param in enumerate(self.experiments[exp].paramsets)]) + '\n'
                    +'################################################################################'
                )
    
    
    def run_one_exp(self, experiment, index):
        
        # make subexp data dir
        os.makedirs(experiment.subexp_dirs[index], exist_ok=False)
                
        self.status.activity = ACTIVITIES.EXP
        self.status.focus = experiment
        self.status.sub_ind = index
        self.status.params = experiment.paramsets[index]
        self.status.data_dir = experiment.subexp_dirs[index]
        
        # set some environment variablves for the benefit of any downstream shells
        os.environ['XANITY_DEBUG'] = str(self.args.debug)
        os.environ['XANITY_LOGGING'] = str(self.args.logging)
        os.environ['XANITY_DATA_DIR'] = str(experiment.subexp_dirs[index])
        
        if not self.args.debug:
            tfh = logging.FileHandler(filename=path.join(experiment.subexp_dirs[index], experiment.name + '.log'))
            tfh.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s: %(message)s'))
            tfh.setLevel(logging.DEBUG)
            self.logger.addHandler(tfh)
    
        self.logger.info("\n"
          "################################################################################\n"
          "## \n"
          "##   starting experiment #{} ({}/{}) \'{}\'\n"
          "##   {}\n"
          "## \n"
          "################################################################################\n"
          "\n".format(index, index + 1, len(experiment.success), experiment.name, self.status.params))
    
        try:

            # import the experiment
            module = _get_live_module_object(experiment.module)
            
            opwd = os.getcwd()
            os.chdir( self.status.data_dir )
            if self.args.profile:
                profile.runctx(
                    'module.main(**paramdict)',
                    {},
                    {'module': module, 'paramdict': self.status.params},
                    path.join(experiment.subexp_dirs[index], experiment + '.profile'))
            else:
                module.main(**self.status.params)
    
            os.chdir(opwd)
            experiment.success[index] = True
            self.logger.info('experiment {} was successful'.format(experiment.name))
    
        except KeyboardInterrupt as e:
            self.savemetadata()
            raise e
    
        except Exception:
            msg = traceback.print_exc()
            if msg is not None:
                self.logger.error(msg)
    
            experiment.success[index] = False
            self.logger.info('experiment {} was NOT successful'.format(experiment.name))
    
        finally:
            if 'tfh' in locals():
                self.logger.removeHandler(tfh)
    
    def run_all_exps(self):
        # do all experiments of interest
        self.n_total_exps = sum([len(item.success) for item in self.experiments.values()])
        
        if self.experiments:
            # make data dir --- should be brand spanking new -- but just in case....
            os.makedirs(self.exp_data_dir, exist_ok=True)
            
            self.run_exp_prelude()
            
            for experiment in self.experiments.values():
                for index, _ in enumerate(experiment.success):
                    self.run_one_exp(experiment, index)

    def run_one_anal(self, analysis, experiment, analysis_ind=None, exp_ind=None):
        
        self.status.activity = ACTIVITIES.ANAL
        self.status.focus = analysis
        self.status.sub_ind = experiment
        self.status.data_dir = experiment.exp_dir
        
        # set some environment variablves for the benefit of any children's shells
        os.environ['XANITY_DEBUG'] = str(self.args.debug)
        os.environ['XANITY_LOGGING'] = str(self.args.logging)
        os.environ['XANITY_DATA_DIR'] = str(experiment.exp_dir)

#        if not self.args.debug:
#            tfh = logging.FileHandler(filename=path.join(self.analyses[analysis].subexp_dirs[index], analysis + '.log'))
#            tfh.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s: %(message)s'))
#            tfh.setLevel(logging.DEBUG)
#            self.logger.addHandler(tfh)
    
        self.logger.info("""
########################################################
  
        starting analysis:  {} (#{} of {})
            -  experiment:  {} (#{} of {})
            - total anals:  {}

########################################################
          """.format(
          analysis.name,  analysis_ind+1,  len(self.analyses),
          experiment.name,  exp_ind+1, len(analysis.experiments),
          self.n_total_anals
          ))

        # import the experiment
        module = _get_live_module_object(analysis.module)

        try:
            if self.args.profile:
                profile.runctx(
                    'module.main(data_dir)',
                    {},
                    {'module': module, 'data_dir': self.status.data_dir},
                    path.join(self.status.data_dir, analysis.name + '.profile'))
            else:
                module.main(self.status.data_dir)
    
            analysis.success.append(True)
            self.logger.info('analysis {} was successful'.format(analysis.name))
    
        except KeyboardInterrupt as e:
            self.savemetadata()
            raise e
    
        except Exception:
            msg = traceback.print_exc()
            if msg is not None:
                self.logger.error(msg)
    
            analysis.success.append(False)
            self.logger.info('analysis {} was NOT successful'.format(analysis.name))
    
        #finally:
            #if 'tfh' in locals():
                #self.logger.removeHandler(tfh)
    
    def run_all_anals(self):
        self.n_total_anals = sum([len(item.experiments) for item in self.analyses.values()])
        
        # do all analyses
        if self.analyses:
            for anal_ind, analysis in enumerate(self.analyses.values()):
                analysis.success = []
                for exp_ind, exp in enumerate(analysis.experiments.values()):
                    self.run_one_anal(analysis, exp, anal_ind, exp_ind)

    def run_hook(self):
        self.run_basic_prelude()
        self.run_all_exps()
        self.run_all_anals()
        
    def list_avail_experiments(self):
        exps = [file.split('.')[0] for file in fnmatch.filter(os.listdir(self.paths.experiments), '[!_]*.py')]
        exps.sort()
        paths = [path.join(self.paths.experiments, exp+'.py' ) for exp in exps]
        return zip(exps, paths)
    
    def list_avail_analyses(self):
        anals = [file.split('.')[0] for file in fnmatch.filter(os.listdir(self.paths.analyses), '[!_]*.py')]
        anals.sort()
        paths = [path.join(self.paths.analyses, anal+'.py' ) for anal in anals]
        return zip(anals, paths)
    
    def load_checkpoint(self, checkpoint_name):
        cp_file = path.join(self.paths.persistent_data, checkpoint_name)
    
        if self.args.loadcp and path.isfile(cp_file):
            return cp_file
        else:
            return None

    def save_checkpoint(self, checkpoint_name):
        cp_file = path.join(self.paths.persistent_data, checkpoint_name)
    
        if self.args.savecp and not path.isfile(cp_file):
            # save it
            return cp_file
        else:
            return path.join(self.exp_data_dir, checkpoint_name)
    
    def save_variable(self, value):
        name = stack(1)[1][4][0].split('(')[1].split(')')[0]
        datapath = path.join(self.status.data_dir, DIRNAMES.SAVED_VARS)
        os.makedirs(datapath, exist_ok=True)
        with open(path.join(datapath, name+'.dill'), 'wb') as f:
            pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)
    
    def load_variable(self, name):            
        datapaths = []
        for base, sdirs, files in os.walk(self.status.data_dir):
            sdirs.sort()
            if DIRNAMES.SAVED_VARS in sdirs:
                datapaths.append(path.join(base, DIRNAMES.SAVED_VARS))
        
        vals = []
        for dpath in datapaths:
            with open(path.join(dpath, name+'.dill'), 'rb') as f:
                vals.append(pickle.load(f, pickle.HIGHEST_PROTOCOL))
        
        return vals, datapaths
    
    def log(self, message):
        self.logger.info(message)

    def _trip_hooks(self, item, hookname):
        """ this will trip all hooks.  
        they each will check self.status.activity to see whether it's appropriate
        to fire"""
        
        assert hookname in dir(self), 'thats not a hook'
        self.status.tripping = hookname
        self.status.focus = item
        fakesies = _get_live_module_object(item.module)
        self.status.focus = None
        self.status.tripping = None
        del fakesies

    def _catch_trip(self):
        if self.status.tripping == stack()[1][3]:
            return True
        else:
            return False
        
    """
    The following are all hooks which can be placed inside analyses and experiments.
    """
    def experiment_parameters(self, parameters_dict):
        if self._catch_trip():
            self.status.focus.param_dict = parameters_dict
        
    def associated_experiments(self, experiment_list):
        if self._catch_trip():
            assert all([ name in self.avail_experiments for name in experiment_list]), 'list contains an unknown xanity experiment'
            self.status.focus.experiments.update({exp: self.avail_experiments[exp] for exp in experiment_list})
            [self.avail_experiments[name].analyses.update({self.status.focus.name: self.status.focus}) for name in experiment_list]
        
    def analyze_this(self):
        if self._catch_trip():
            cand_anals = list(filter(lambda item: self.status.focus.name in item.experiments, self.avail_analyses.values()))
            for anal in cand_anals:
                if anal.name not in self.analyses:
                    self.analyses.update({anal.name: anal})
            
    