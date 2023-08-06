#!/usr/bin/env python
## pytest tests

import subprocess
import os
from . import common

def test_init_here(test_proj_here, capfd):
	proj_name = test_proj_here[0]
	proj_path = test_proj_here[1]
	os.chdir(proj_path)

	os.makedirs(proj_name)
	os.chdir(proj_name)

	subprocess.call(['bash','xanity','init'])

	assert 'created' in capfd.readouterr().out
	assert common.ls_skel_diff(proj_name) == ''

	subprocess.call(['bash','git','status'])

	assert 'not a repository' not in capfd.readouterr().out


def test_init_other(test_proj_other, capfd):
	proj_name = test_proj_other[0]
	proj_path = test_proj_other[1]
	os.chdir(proj_path)

	subprocess.call(['bash','xanity','init',proj_name])

	assert 'created' in capfd.readouterr().out
	assert common.ls_skel_diff(proj_name) == ''

	subprocess.call(['bash','git','status'])

	assert 'not a repository' not in capfd.readouterr().out


