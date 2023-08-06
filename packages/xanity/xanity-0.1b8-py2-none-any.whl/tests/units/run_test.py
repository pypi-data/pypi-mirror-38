#!/usr/bin/env python
## pytest tests

import pytest
import subprocess
import os
from os.path import join as pathjoin
import re

def run_here():
	proj_name = test_proj_here

	os.chdir(proj_name)

	treetop1 = subprocess.check_output('bash ls -a data/runs')
	tree1 = subprocess.check_output('bash ls -ar data/runs')

	msg = subprocess.check_output('bash xanity run')

	treetop2 = subprocess.check_output('bash ls -a data/runs')
	tree2 = subprocess.check_output('bash ls -ar data/runs')

	assert 'created' in msg
	assert treetop1 != treetop2
	assert tree1 != tree2

def run_other():
	proj_name = test_proj_other

	msg = subprocess.check_output(['bash xanity run', proj_name])

	treetop1 = subprocess.check_output(['bash ls -a', pathjoin(proj_name,data,runs)])
	tree1 = subprocess.check_output(['bash ls -ar', pathjoin(proj_name,data,runs)])

	msg = subprocess.check_output(['bash xanity run', proj_name])

	treetop2 = subprocess.check_output(['bash ls -a', pathjoin(proj_name,data,runs)])
	tree2 = subprocess.check_output(['bash ls -ar', pathjoin(proj_name,data,runs)])

	assert 'created' in msg
	assert treetop1 != treetop2
	assert tree1 != tree2