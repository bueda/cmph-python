#!/usr/bin/env python
import os
from fabric.api import *

from fab_shared import _nose_test_runner, _test, _package_deploy

env.unit = "cmph-python"
env.root_dir = os.path.abspath(os.path.dirname(__file__))
env.scm = env.root_dir
env.allow_no_tag = True
env.upload_to_s3 = True
env.test_runner = _nose_test_runner
 
def deploy(release=None, skip_tests=None):
    _build()
    _package_deploy(release, skip_tests)

@runs_once
def test(dir=None):
    _build()
    _test(dir)

def _build():
    with cd(env.root_dir):
        local('python setup.py build', capture=False)
        local('python setup.py build_ext --inplace', capture=False)
