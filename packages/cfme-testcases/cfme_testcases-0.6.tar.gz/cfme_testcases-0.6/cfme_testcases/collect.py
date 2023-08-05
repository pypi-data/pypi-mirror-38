# -*- coding: utf-8 -*-
"""
Run pytest --collect-only and generate JSONs.
"""

from __future__ import absolute_import, unicode_literals

import logging
import os
import subprocess
import sys

from cfme_testcases import consts
from cfme_testcases.exceptions import TestcasesException

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


_JSON_FILES = (consts.TEST_CASE_JSON, consts.TEST_RUN_JSON)


def jsons_ready(testcases_json, testsuites_json, testsuites_needed):
    """Check if the needed JSON files are already available."""
    # if the file names were passed, check that the files exist
    if testcases_json and not os.path.exists(testcases_json):
        raise TestcasesException(
            "The testcases JSON file `{}` doesn't exist.".format(testcases_json)
        )
    if testsuites_needed and testsuites_json and not os.path.exists(testsuites_json):
        raise TestcasesException(
            "The testsuites JSON file `{}` doesn't exist.".format(testsuites_json)
        )

    if not testcases_json:
        return False
    if testsuites_needed and not testsuites_json:
        return False
    return True


def collect_testcases(pytest_collect, testcases_json, testsuites_json, testsuites_needed=False):
    """Collects testcases data."""
    retval = None

    if not jsons_ready(testcases_json, testsuites_json, testsuites_needed):
        testcases_json, testsuites_json = _JSON_FILES
        retval = run_pytest(pytest_collect)

    return retval, testcases_json, testsuites_json


def check_jsons():
    """Check that the JSON files were generated."""
    missing_files = []
    for fname in _JSON_FILES:
        if not os.path.exists(fname):
            missing_files.append(fname)
    if missing_files:
        raise TestcasesException(
            "The JSON file(s) `{}` doesn't exist.".format(" and ".join(missing_files))
        )


def check_environment():
    """Checks the environment for running pytest."""
    if not os.path.exists(".git"):
        raise TestcasesException("Not launched from the top-level directory.")
    # check that running in virtualenv
    if not hasattr(sys, "real_prefix"):
        raise TestcasesException("Not running in virtual environment.")


def cleanup():
    """Deletes JSON files generated during previous runs."""
    for fname in _JSON_FILES:
        try:
            os.remove(fname)
        except OSError:
            pass


def run_pytest(pytest_collect):
    """Runs the pytest command."""
    if not pytest_collect:
        raise TestcasesException(
            "The `pytest_collect` command for collecting testcases was not specified."
        )

    pytest_retval = 250
    check_environment()
    cleanup()

    pytest_args = pytest_collect.split(" ")

    logger.info("Generating the JSONs using '%s'", pytest_collect)
    with open(os.devnull, "w") as devnull:
        pytest_proc = subprocess.Popen(pytest_args, stdout=devnull, stderr=devnull)
        try:
            pytest_retval = pytest_proc.wait()
        # pylint: disable=broad-except
        except Exception:
            try:
                pytest_proc.terminate()
            except OSError:
                pass
            pytest_proc.wait()

    check_jsons()
    return pytest_retval
