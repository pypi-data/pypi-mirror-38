import dill as pickle
import fnmatch
import tarfile
import json
import inspect
import os
import os.path as path
import logging
import sys
import argparse
import importlib
import time
import traceback
import cProfile as profile
import datetime

from copy import deepcopy

try:
    from pip._internal.operations import freeze
except ImportError:
    from pip.internal.operations import freeze
    
path_defs = {'src':'src',
             'include':'include',
             'experiments':'experiments',
             'analyses':'analyses',
             'run_data':'data/runs',
             'persistent_data':'data/persistent',
             'saved_data':'data/saved',
             'xanity_data':'.xanity'}


class Xanity:
    
    def __init__(self, clargs=None):
        self.start_time = time.localtime()
        self.xanity_root = self.resolve_xanity_root()
        self.name = self.xanity_root.split('/')[-1]
        self.paths = {key: os.path.join(self.xanity_root, value) for key, value in path_defs.items()}
        self.experiments = {name: {} for name in self.list_avail_experiments()}
        self.analyses = {name: {} for name in self.list_avail_analyses()}
        
        self._parse_args(clargs)
        
        if self.args.debug:
            self.data_dir = os.path.join(self.paths['run_data'], '{}-debug'.format(time.strftime('%Y-%m-%d-%H%M%S', self.start_time)))
        else:
            self.data_dir = os.path.join(self.paths['run_data'], '{}'.format(time.strftime('%Y-%m-%d-%H%M%S', self.start_time)))
        # make data dir --- should be brand spanking new
        os.makedirs(self.data_dir, exist_ok=False)
        
        # put experiments on path
        sys.path.append(self.paths['experiments'])
        
        self._init_logger()
        self._resolve_experiments_of_interest()
        self._resolve_exp_sigs()
        self._parse_sub_exps()

        self.status = {}
        
    def _parse_sub_exps(self):
        """see if any experiments have asked for param-sets """

        if isinstance(self.experiments, list):
            self.experiments = {item: {} for item in self.experiments}
            
        for experiment in self.experiments.keys():
            ldict = dict()
    
            try:
                exec('from {} import EXPERIMENT_PARAMETERS'.format(experiment), {}, ldict)
            except ImportError as e:
                if 'EXPERIMENT_PARAMETERS' in e.msg:
                    ldict['EXPERIMENT_PARAMETERS']=None
                else:
                    raise e
    
            if ldict['EXPERIMENT_PARAMETERS']:
                paramsets = ldict['EXPERIMENT_PARAMETERS']
        
                for key, value in paramsets.items():
                    if type(value) is not list:
                        paramsets[key] = [value]
        
                # get number of subexperiments
                nametup = tuple(paramsets.keys())
                kwlens = tuple(len(paramsets[key]) for key in list(nametup))
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
                self.experiments[experiment].update({
                    'data_dirs': [ path.join(self.data_dir,'{}-{}'.format(experiment, i)) for i in enumerate(indvec)],
                    'success': [False]*len(indvec),
                    'paramsets': [ {nametup[i]: nametup[i][choice] for i,choice in enumerate(vect)} for vect in indvec ],
                })
            
            else:
                # create single subexperiment directory
                self.experiments[experiment].update({
                        'data_dirs': [path.join(self.data_dir,experiment)],
                        'success': [False],
                        'paramsets': [self.experiments[experiment]['parameter_sig']],
                })

    def _resolve_experiments_of_interest(self):
        """ find out what experiments we're going to run """
        
        ## already done ## sys.path.append(self.paths['experiments'])
    
        if self.args.experiments:
            expreqd = self.args.experiments
            if ' ' in expreqd:
                expreqd = expreqd.split(' ')
            elif isinstance(expreqd, str):
                expreqd = [expreqd]
    
            for item in expreqd:
                if item not in self.experiments:
                    #metadata['logger'].error('couldn\'t find \"{}\" in experiments directory...'.format(item))
                    #metadata['logger'].info('aborting...')
                    raise IOError('couldnt find experiment named {}.'.format(item))
            experimentlist = expreqd
    
        else:
            experimentlist = self.experiments
    
        self.experiments_of_interest = experimentlist
        
    def _init_logger(self):
        """ setup a logger ... """
        # create logger
        self.logger = logging.getLogger('xanity_logger')
        self.logger.handlers = []
        self.logger.setLevel(logging.DEBUG)
        
        lfh = logging.FileHandler(filename=os.path.join(self.data_dir, 'root.log'))
        lfh.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s: %(message)s'))
        lfh.setLevel(logging.DEBUG)
        self.logger.addHandler(lfh)
        
        lsh = logging.StreamHandler(sys.stdout)
        lsh.setFormatter(logging.Formatter(self.data_dir.split('/')[-1] + ' %(asctime)s :%(levelname)s: %(message)s'))
        lsh.setLevel(logging.DEBUG)
        self.logger.addHandler(lsh)
        
    def _resolve_exp_sigs(self):
        """ see if there are any parameter sets given for the exp """
        for experiment in self.experiments.keys():
            ldict = dict()
        
            try:
                exec('from {} import main'.format(experiment), {}, ldict)
            except ImportError as e:
                if 'main(' in e.msg:
                    pass
                else:
                    raise e
        
            sig = inspect.signature(ldict['main'])
            
            self.experiments[experiment]['parameter_sig'] = {parameter.name: parameter.default for parameter in sig.parameters.values()}

    def _parse_args(self, clargs=None):
        """ parse arguments """
    
        parser = argparse.ArgumentParser()
        parser.add_argument('experiments', nargs='*', default=self.list_avail_experiments(),
                            help='specify the experiments you wish to run and/or process')
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
        parser.add_argument('-A', '--analyze-only', action='store',
                            help='don\'t conduct experiment, only analyze data. data to be specified in following argument:'
                                 '  -A [--analyze-only] 2018-10-29-0100 myExperiment1')
        parser.add_argument('-a', '--and-analyze', action='store_true',
                            help='requests that data be analyzed upon completion of experiment')
    
        if not clargs:
            self.command = ' '.join(sys.argv)
            self.args, self.unknownargs = parser.parse_known_args()
            if ' ' not in self.command:
                # single file called as script
                self.args.experiments = self.command.split('/')[-1].rstrip('.py')
        else:
            self.args, self.unknownargs = parser.parse_known_args(clargs)

    def archive_source_tree(self):
    
        if not self.args.debug:
            # make requirements.txt
            reqs = freeze.freeze()
            with open(path.join(self.data_dir, 'requirements.txt'), mode='w') as reqsfile:
                for line in reqs:
                    reqsfile.write(line + '\n')
    
            filterfn = lambda tarinfo: None if fnmatch.fnmatch(tarinfo.name, '*/data/*') or fnmatch.fnmatch(tarinfo.name, '*/data') else tarinfo
            with tarfile.open(path.join(self.data_dir, 'source.tar.gz'), mode='w:gz') as tarball:
                tarball.add(self.xanity_root, arcname=self.name, filter=filterfn)

            ## dump tarballs of source
            #if os.path.isdir(os.path.join(data_dir, 'src')):
            #    tarball = tarfile.open(path.join(self.data_dir, 'src.tar.gz'), mode='w:gz')
            #    tarball.add(src_dir, arcname='src')
            #    tarball.close()
    
            ## dump tarballs of libraries
            #if os.path.isdir(os.path.join(data_dir, 'lib')):
            #    tarball = tarfile.open(path.join(self.data_dir, 'lib.tar.gz'), mode='w:gz')
            #    tarball.add(xanity_root + '/lib', arcname='lib')
            #    tarball.close()
    
            ## dump tarballs of includes
            #if os.path.isdir(os.path.join(data_dir, 'inc')):
            #    tarball = tarfile.open(os.path.join(self.data_dir, 'include.tar.gz'), mode='w:gz')
            #    tarball.add(xanity_root + '/include', arcname='include')
            #    tarball.close()

    def savemetadata(self):
        data = deepcopy(self)
        del data.logger
        with open(path.join(self.data_dir, 'xanity_metadata.dill'), mode='wb') as f:
            json.dump(data, f)
            
    def resolve_xanity_root(self):
        """ set xanity_root """
    
        pwd = os.getcwd()
        path_parts = pwd.split('/')
    
        for i in range(len(path_parts))[::-1]:
            test_path = '/'+path.join(*path_parts[:i+1])
            if path.isdir(path.join(test_path,'.xanity')):
                return test_path
    
        raise RuntimeError('xanity not called from within a tree. if you invoke xanity from the command-line, you must be inside a xanity tree')

    def run_prelude(self):
        """
            bunch of meta-level setup for subsequent experiments
        """

        # set global root dirs and do some basic path operations
        os.chdir(self.xanity_root)
    
        # dump a bunch of tarballs
        self.archive_source_tree()
    
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
    
        # print number of subexperiments found:
        for exp in self.experiments.keys():
            if len(self.experiments[exp]['paramsets']) > 1:
                self.logger.info(
                    '\n'
                    '################################################################################\n'
                    '##  experiment: {} has {} subexperiments:\n'.format(exp, len(self.experiments[exp]['paramsets']))
                    +'\n'.join(['##     exp #{}: {}'.format(i,param) for i,param in enumerate(self.experiments[exp]['paramsets'])]) + '\n'
                    +'################################################################################'
                )
    
    def run_one_exp(self, experiment, index):
        
        # make subexp data dir
        os.makedirs(self.experiments[experiment]['data_dirs'][index], exist_ok=False)
        
        paramdict = self.experiments[experiment]['paramsets'][index]
        self.status.update({'experiment': experiment})
        self.status.update({'subexp_ind': index})
        self.status.update({'savepath': self.experiments[experiment]['data_dirs'][index]})
        
        if not self.args.debug:
            tfh = logging.FileHandler(filename=os.path.join(self.experiments[experiment]['data_dirs'][index], experiment + '.log'))
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
          "\n".format(index, index + 1, len(self.experiments[experiment]['paramsets']), experiment, paramdict))
    
        try:
            # import the experiment
            module = importlib.import_module(experiment)
    
            # set some environment variablves for the benefit of any downstream shells
            os.environ['XANITY_DEBUG'] = str(self.args.debug)
            os.environ['XANITY_LOGGING'] = str(self.args.logging)
            os.environ['XANITY_DATA_DIR'] = str(self.experiments[experiment]['data_dirs'][index])
    
            if self.args.profile:
                profile.runctx(
                    'module.main(**paramdict)',
                    {},
                    {'module': module, 'paramdict': paramdict},
                    os.path.join(self.experiments[experiment]['data_dirs'][index], experiment + '.profile'))
            else:
                module.main(**paramdict)
    
            self.experiments[experiment]['success'][index] = True
            self.logger.info('experiment {} was successful'.format(experiment))
    
        except KeyboardInterrupt as e:
            self.savemetadata()
            raise e
    
        except Exception:
            msg = traceback.print_exc()
            if msg is not None:
                self.logger.error(msg)
    
            self.experiments[experiment]['success'][index] = False
            self.logger.info('experiment {} was NOT successful'.format(experiment))
    
        finally:
            if 'tfh' in locals():
                self.logger.removeHandler(tfh)
    
    def run_all_exps(self):
        # do all experiments of interest
        for experiment in self.experiments_of_interest:
            for index, _ in enumerate(self.experiments[experiment]['data_dirs']):
                self.run_one_exp(experiment, index)
    
    def run_one_anal(self, experiment):
        raise NotImplementedError
    
    def list_avail_experiments(self):
        exps = [file.split('.')[0] for file in fnmatch.filter(os.listdir(self.paths['experiments']), '[!_]*.py')]
        exps.sort()
        return exps
    
    def list_avail_analyses(self):
        anals = [file.split('.')[0] for file in fnmatch.filter(os.listdir(self.paths['analyses']), '[!_]*.py')]
        anals.sort()
        return anals
    
    def load_checkpoint(self, checkpoint_name):
        cp_file = os.path.join(self.paths['persistent_data'], checkpoint_name)
    
        if self.args.loadcp and os.path.isfile(cp_file):
            return cp_file
        else:
            return None

    def save_checkpoint(self, checkpoint_name):
        cp_file = os.path.join(self.paths['persistent_data'], checkpoint_name)
    
        if self.args.savecp and not os.path.isfile(cp_file):
            # save it
            return cp_file
        else:
            return os.path.join(self.data_dir, checkpoint_name)
    
    def save_variable(self, name, value):
        os.makedirs(path.join(self.status['savepath'],'xanity_saved_vars'), exist_ok=True)
        with open(path.join(self.status['savepath'],'xanity_saved_vars', name+'.dill'), 'wb') as f:
            pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)
    
    def load_variable(self, name):
        with open(path.join(self.status['savepath'],'xanity_saved_vars', name+'.dill'), 'wb') as f:
            val = pickle.load(f, pickle.HIGHEST_PROTOCOL)
        return val
    
    def log(self, message):
        self.logger.info(message)
