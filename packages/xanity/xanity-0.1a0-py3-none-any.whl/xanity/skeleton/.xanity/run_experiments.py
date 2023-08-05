#!/usr/bin/env python

from __future__ import print_function
import argparse
import importlib
import logging
import os
import sys
import tarfile
import time
import traceback
import cProfile as profile
import datetime
import json
import inspect
import dill as pickle
import fnmatch

try:
    from pip._internal.operations import freeze
except ImportError:
    from pip.internal.operations import freeze

metadata = {}

metadata['xanity_root'] = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1])

metadata['paths'] = {
    'src':'src',
    'include':'include',
    'experiments':'experiments',
    'analyses':'analyses',
    'run_data':'data/runs',
    'persistent_data':'data/persistent',
    'saved_data':'data/saved',
}
metadata['paths'] = {key: os.path.join(metadata['xanity_root'], value) for key, value in metadata['paths'].items()}

def setup():
    """
        bunch of meta-level setup for subsequent experiments
    """
    global metadata

    start_time = time.localtime()

    # set global root dirs and do some basic path operations
    os.chdir(metadata['xanity_root'])

    if not metadata['args'].debug:
        data_dir = os.path.join(metadata['paths']['run_data'], '{}'.format(time.strftime('%Y-%m-%d-%H%M%S', start_time)))
    else:
        data_dir = os.path.join(metadata['paths']['run_data'], '{}-debug'.format(time.strftime('%Y-%m-%d-%H%M%S', start_time)))

    # make data dir
    os.makedirs(data_dir, exist_ok=True)

    # fill in some metadata
    metadata['start_time'] = start_time
    metadata['data_dir'] = data_dir

    # setup a logger ...
    metadata['logger'] = logging.getLogger('xanity_logger')
    metadata['logger'].setLevel(logging.DEBUG)
    
    lfh = logging.FileHandler(filename=os.path.join(data_dir, 'root.log'))
    lfh.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s: %(message)s'))
    lfh.setLevel(logging.DEBUG)
    metadata['logger'].addHandler(lfh)

    lsh = logging.StreamHandler(sys.stdout)
    lsh.setFormatter(logging.Formatter(data_dir.split('/')[-1] + ' %(asctime)s :%(levelname)s: %(message)s'))
    lsh.setLevel(logging.DEBUG)
    metadata['logger'].addHandler(lsh)

    # print some info
    metadata['logger'].info(
        '\n'
        '################################################################################\n'
        '## \n'
        '## \'run\' called at {} \n'
        '## {}\n'
        '## xanity_root: {} \n'
        '################################################################################\n'
        '\n'.format(
            datetime.datetime.fromtimestamp(time.mktime(metadata['start_time'])).strftime('%Y-%m-%d %H:%M:%S'),
            vars(metadata['args']),
            metadata['xanity_root'])
    )

    # find out what experiments we're going to run
    sys.path.append(metadata['paths']['experiments'])
    avail_exps = list_experiments()

    if metadata['args'].experiments:
        expreqd = metadata['args'].experiments
        if ' ' in expreqd:
            expreqd = expreqd.split(' ')
        elif isinstance(expreqd, str):
            expreqd = [expreqd]
        
        if not all([item in avail_exps for item in expreqd]):
            metadata['logger'].error('couldn\'t find \"{}\" in experiments directory...'.format(item))
            metadata['logger'].info('aborting...')
            raise IOError('couldnt find experiment named {}.'.format(item))
        else:
            experimentlist = expreqd

    else:
        experimentlist = avail_exps
        #print('found experiments: {}'.format(experimentlist))

    metadata['experiments'] = dict(zip(experimentlist, [{}] * len(experimentlist)))

    # go through and see if we're iterating over any parameters in the experiments
    for experiment in metadata['experiments']:

        ldict = dict()

        try:
            exec('from {} import EXPERIMENT_PARAMETERS'.format(experiment), {}, ldict)
        except ImportError as e:
            if 'EXPERIMENT_PARAMETERS' in e.msg:
                pass
            else:
                raise e

        try:
            exec('from {} import main'.format(experiment), {}, ldict)
        except ImportError as e:
            if 'main(' in e.msg:
                pass
            else:
                raise e

        (names, _, _, defargs) = inspect.getargspec(ldict['main'])
        dfp = {names[i]: defargs[i] for i in range(len(names)) if names[i] != 'data_dir' and names[i] != 'metadata'}
        del names
        del defargs

        if 'EXPERIMENT_PARAMETERS' in ldict and ldict['EXPERIMENT_PARAMETERS']:
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
            nsubexps = len(indvec)

            # create all the subexperiment info
            metadata['experiments'][experiment]['data_dirs'] = list()
            metadata['experiments'][experiment]['success'] = list()
            metadata['experiments'][experiment]['paramsets'] = list()

            # create directories
            for index in range(nsubexps):
                paraminds = indvec[index]
                tdict = {}
                for key, val in dfp.items():
                    if key in nametup:
                        tdict.update({key: paramsets[key][paraminds[nametup.index(key)]]})
                    else:
                        tdict.update({key: val})
                metadata['experiments'][experiment]['paramsets'].append(tdict)
                metadata['experiments'][experiment]['data_dirs'].append(
                    os.path.join(metadata['data_dir'], experiment + '-' + str(index)))
                metadata['experiments'][experiment]['success'].append(False)

                # create per-subexperiment directories
                os.mkdir(metadata['experiments'][experiment]['data_dirs'][index])

                # in it, create a file to catalog the parametric values
                with open(
                        os.path.join(
                            metadata['experiments'][experiment]['data_dirs'][index],
                            'EXPERIMENT_PARAMETERS.json'),
                        mode='w') as file:
                    json.dump(metadata['experiments'][experiment]['paramsets'][index], file)
        else:
            # create per- subexperiment directory
            metadata['experiments'][experiment].update({
                'data_dirs': [os.path.join(metadata['data_dir'], experiment)],
                'success': [False],
            })
            os.mkdir(metadata['experiments'][experiment]['data_dirs'][0])
            metadata['experiments'][experiment]['paramsets'] = [{}]

    # print number of subexperiments found:
    for exp in metadata['experiments']:
        if 'paramsets' in metadata['experiments'][exp]:
            metadata['logger'].info(
                '\n'
                '################################################################################\n'
                '##  experiment: {} has {} subexperiments:\n'.format(exp, len(metadata['experiments'][exp]['paramsets']))
                +'\n'.join(['##     exp #{}: {}'.format(i,param) for i,param in enumerate(metadata['experiments'][exp]['paramsets'])]) + '\n'
                +'################################################################################'
            )

    # dump a bunch of tarballs
    if not metadata['args'].debug:

        # make requirements.txt
        reqs = freeze.freeze()
        with open(os.path.join(data_dir, 'requirements.txt'), mode='w') as reqsfile:
            for line in reqs:
                reqsfile.write(line + '\n')

        # dump tarballs of source
        if os.path.isdir(os.path.join(data_dir, 'src')):
            tarball = tarfile.open(os.path.join(data_dir, 'src.tar.gz'), mode='w:gz')
            tarball.add(src_dir, arcname='src')
            tarball.close()

        # dump tarballs of libraries
        if os.path.isdir(os.path.join(data_dir, 'lib')):
            tarball = tarfile.open(os.path.join(data_dir, 'lib.tar.gz'), mode='w:gz')
            tarball.add(xanity_root + '/lib', arcname='lib')
            tarball.close()

        # dump tarballs of includes
        if os.path.isdir(os.path.join(data_dir, 'inc')):
            tarball = tarfile.open(os.path.join(data_dir, 'include.tar.gz'), mode='w:gz')
            tarball.add(xanity_root + '/include', arcname='include')
            tarball.close()


def runit(experiment, index):
    global metadata

    try:
        paramdict = metadata['experiments'][experiment]['paramsets'][index]
    except KeyError:
        paramdict = None

    if not metadata['args'].debug:
        tfh = logging.FileHandler(
            filename=os.path.join(metadata['experiments'][experiment]['data_dirs'][index], experiment + '.log'))
        tfh.setFormatter(logging.Formatter('%(asctime)s :%(levelname)s: %(message)s'))
        tfh.setLevel(logging.DEBUG)
        metadata['logger'].addHandler(tfh)

    metadata['logger'].info("\n"
                            "################################################################################\n"
                            "## \n"
                            "##   starting experiment #{} ({}/{}) \'{}\'\n"
                            "##   {}\n"
                            "## \n"
                            "################################################################################\n"
                            "\n".format(index, index + 1, len(metadata['experiments'][experiment]['paramsets']),
                                        experiment, paramdict))

    try:
        # import the experiment
        module = importlib.import_module(experiment)

        # set some environment variablves
        os.environ['PYTHEX_DEBUG'] = str(metadata['args'].debug)
        os.environ['PYTHEX_LOGGING'] = str(metadata['args'].logging)
        os.environ['PYTHEX_DATA_DIR'] = str(metadata['experiments'][experiment]['data_dirs'][index])

        if metadata['args'].profile:

            profile.runctx(
                'module.main( metadata=metadata,'
                '**paramdict)',
                {},
                {
                    'module': module,
                    'metadata': metadata,
                    'paramdict': paramdict,
                    'experiment': experiment,
                    'index': index
                },
                os.path.join(metadata['experiments'][experiment]['data_dirs'][index], experiment + '.profile'))
        else:
            module.main(**paramdict,
                        metadata=metadata,
                        )

        metadata['experiments'][experiment]['success'][index] = True
        metadata['logger'].info('experiment {} was successful'.format(experiment))

    except KeyboardInterrupt:
        savemetadata()
        sys.exit()

    except Exception:
        msg = traceback.print_exc()
        if msg is not None:
            metadata['logger'].error(msg)

        metadata['experiments'][experiment]['success'][index] = False
        metadata['logger'].info('experiment {} was NOT successful'.format(experiment))

    finally:
        if 'tfh' in locals():
            metadata['logger'].removeHandler(tfh)


def main(*args):
    """
        look in experiments folder and run all or passed selection
     """
    global metadata

    # pars arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('experiments', nargs='*', default=None,
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
    parser.add_argument('-P', '--process-only', action='store',
                        help='don\'t conduct experiment, only process data. data to be specified in following argument:'
                             '  -P [--process-onlu] myExperiment01')
    parser.add_argument('-p', '--and-process', action='store_true',
                        help='requests that data be processed upon completion of experiment')
    
    if __name__ == '__main__':
        metadata['command'] = ' '.join(sys.argv)
        metadata['args'], metadata['unknownargs'] = parser.parse_known_args()
    elif args:
        metadata['args'], metadata['unknownargs'] = parser.parse_known_args(args)
    else:
        raise NotImplementedError

    if metadata['args'].process_only:
        #process.main(metadata=metadata)
        sys.exit(0)

    else:
        setup()
        savemetadata()
        metadata['status'] = {}
        for experiment in metadata['experiments']:
            for index in range(len(metadata['experiments'][experiment]['data_dirs'])):
                metadata['status'].update({'experiment': experiment})
                metadata['status'].update({'subexp_ind': index})
                metadata['status'].update({'savepath': metadata['experiments'][experiment]['data_dirs'][index]})
                runit(experiment, index)
                savemetadata()

        successful = list()
        for (exp, result) in metadata['experiments'].items():
            if any(result['success']):
                successful.append(exp)

        if metadata['args'].and_process:
            for exp in metadata['experiments']:
                for i, datadir in enumerate(metadata['experiments'][exp]['data_dirs']):
                    if metadata['experiments'][exp]['success'][i]:
                        #process.main(metadata=metadata)
                        break
        sys.exit(0)


def savemetadata():
    dd = dict(metadata)
    dd.pop('logger')
    dd.update({'args': vars(dd['args'])})
    with open(os.path.join(metadata['data_dir'], 'METADATA.json'), mode='w') as file:
        json.dump(dd, file)


def load_checkpoint(checkpoint_name, metadata):
    cp_file = os.path.join(persistent_data_path, checkpoint_name)

    if metadata['args'].loadcp and os.path.isfile(cp_file):
        return cp_file
    else:
        return None


def save_checkpoint(checkpoint_name, metadata):
    cp_file = os.path.join(persistent_data_path, checkpoint_name)

    if metadata['args'].savecp and not os.path.isfile(cp_file):
        # save it
        return cp_file
    else:
        return os.path.join(metadata['data_dir'], checkpoint_name)


def save_variables(item, filename):
    with open(filename, 'wb') as f:
        pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

def list_experiments():
    exps = [file.split('.')[0] for file in fnmatch.filter(os.listdir(metadata['paths']['experiments']), '[!_]*.py')]
    exps.sort()
    return exps

if __name__ == '__main__':
    main()
