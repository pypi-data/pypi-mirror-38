#!/usr/bin/env python

import importlib
import os
from os.path import join as pathjoin
from xanity import common


def getdatadefinitions():
    exps = experiments.lsmodules()
    defs = dict()

    for exp in exps:
        try:
            mylcdic = dict()
            exec('from experiments.'+exp+' import DATA_DEFINITION', {}, mylcdic)
            defs.update({exp: mylcdic['DATA_DEFINITION']})
        except ImportError:
            raise NotImplementedError('You must provide a module-level variable called'
                                      ' DATA_DEFINITION in your experiment.')
    return defs


#def lsmodules():
#    import os
#    exp_dir = os.path.dirname(os.path.abspath(__file__))
#    dirlist = os.listdir(exp_dir)
#    items = [item[:-3] if item.endswith('.py') else False for item in dirlist]
#    items = [item for item in filter(bool, items)]
#    items = [item for item in filter(lambda x: x != '__init__', items)]
#    items = sorted(items)
#    return items


def main(metadata=None):
    if metadata['args'].process_only is not False:
        expnames = metadata['args'].experiments
        expdir = metadata['args'].process_only if isinstance(metadata['args'].process_only, str) else None

        for expname in expnames:
            if expdir is None:
                cands = []
                for dirs, subdirs, files in os.walk('./run_data', followlinks=False):
                    if expname in subdirs:
                        cands.append(dirs)
                cands = sorted(cands, key=str.lower)
                data_dir = pathjoin(cands[-1], expname)

            else:
                if expdir in os.listdir('./run_data'):
                    data_dir = pathjoin('.', 'run_data', expdir, expname)
                elif os.path.isdir('./saved_runs') and expdir in os.listdir('./saved_runs'):
                    cands = []
                    for dirs, subdirs, files in os.walk(pathjoin('./saved_runs', expdir), followlinks=False):
                        for subdir in subdirs:
                            if expname in subdir:
                                cands.append((dirs, subdir))
                    cands = sorted(cands, key=lambda item: item[0].lower())
                    cands.reverse()
                    data_dir = [pathjoin(cand[0], cand[1]) for cand in cands]
                else:
                    raise FileNotFoundError

            a = importlib.import_module('.' + expname, package='process')
            a.main(data_dir=data_dir, metadata=metadata)

    else:
        for expname in metadata['experiments'].keys():
            a = importlib.import_module('.' + expname, package='process')
            a.main(data_dir=metadata['experiments'][expname]['data_dirs'], metadata=metadata)


__all__ = ['lsmodules']
