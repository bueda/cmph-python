#!/usr/bin/env python
import os
from fabric.api import *
from fabric.contrib.console import confirm

from fab_shared import _nose_test, _test, _package_deploy

env.unit = "cmph-python"
env.root_dir = os.path.abspath(os.path.dirname(__file__))
env.scm = env.root_dir
env.allow_no_tag = True
env.upload_to_s3 = True
 
def deploy(release=None, skip_tests=None):
    local('python setup.py build', capture=False)
    local('python setup.py build_ext --inplace', capture=False)
    _package_deploy(release, skip_tests)

@runs_once
def test(dir=None):
    local('python setup.py build', capture=False)
    local('python setup.py build_ext --inplace', capture=False)
    _test(_nose_test)
