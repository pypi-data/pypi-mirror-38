#!/usr/bin/env python
## pytest tests

import pytest
import subprocess
import os
from os.path import join as pathjoin

def setup_here():
	proj_name = test_proj_here

	os.chcwd(proj_name)
	msg = subprocess.check_output('bash xanity setup')

	assert 'created' in msg
	assert os.isfile(proj_name,'.xanity','setupcomplete')
	assert os.isfile(proj_name,'.xanity','UUID')
	assert 'not a repository' not in subprocess.check_output('bash git status')

def setup_other():
	proj_name = test_proj_other

	msg = subprocess.check_output(['bash xanity setup', proj_name])

	assert 'created' in msg
	assert os.isfile(proj_name,'.xanity','setupcomplete')
	assert os.isfile(proj_name,'.xanity','UUID')
	assert 'not a repository' not in subprocess.check_output('bash git status')