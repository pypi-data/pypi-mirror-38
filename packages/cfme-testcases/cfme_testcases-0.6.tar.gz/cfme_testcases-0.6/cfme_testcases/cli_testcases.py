# -*- coding: utf-8 -*-
"""
Create new testrun and upload missing testcases using Polarion Importers.
"""

from __future__ import absolute_import, unicode_literals

import datetime
import logging
import os
import threading

from cfme_testcases import cli_utils, consts, gen_xmls
from cfme_testcases.exceptions import NothingToDoException, TestcasesException
from dump2polarion import properties, submit
from dump2polarion import utils as d2p_utils

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


class TestcasesSubmitter(object):
    """Submits filtered XMLs."""

    def __init__(self, args, submit_args, config, filtered_xmls):
        self.args = args
        self.submit_args = submit_args
        self.config = config
        self.filtered_xmls = filtered_xmls
        self._succeeded = []
        self._failed = []

    def _get_job_log(self, prefix):
        job_log = None
        if self.args.output_dir:
            job_log = "job-{}-{}.log".format(prefix, cli_utils.get_filename_str(self.args))
            job_log = os.path.join(self.args.output_dir, job_log)
        return job_log

    def update_existing_testcases(self):
        """Updates existing testcases in new thread."""
        output = []
        updating_testcases_t = None

        job_log = self._get_job_log("update")
        all_submit_args = dict(
            xml_root=self.filtered_xmls.updated_testcases,
            config=self.config,
            log_file=job_log,
            **self.submit_args
        )

        # run it in separate thread so we can continue without waiting
        # for the submit to finish
        def _run_submit(results, args_dict):
            retval = submit.submit_and_verify(**args_dict)
            results.append(retval)

        updating_testcases_t = threading.Thread(target=_run_submit, args=(output, all_submit_args))
        updating_testcases_t.start()

        return updating_testcases_t, output

    def create_missing_testcases(self):
        """Creates missing testcases in Polarion."""
        job_log = self._get_job_log("testcases")
        retval = submit.submit_and_verify(
            xml_root=self.filtered_xmls.missing_testcases,
            config=self.config,
            log_file=job_log,
            **self.submit_args
        )
        return retval

    def add_missing_testcases_to_testrun(self):
        """Adds missing testcases to testrun."""
        job_log = self._get_job_log("testrun")
        retval = submit.submit_and_verify(
            xml_root=self.filtered_xmls.missing_testsuites,
            config=self.config,
            log_file=job_log,
            **self.submit_args
        )
        return retval

    def _append_msg(self, retval, msg):
        if retval:
            self._succeeded.append(msg)
        else:
            self._failed.append(msg)

    def _log_outcome(self):
        if self._succeeded and self._failed:
            logger.info("SUCCEEDED to %s", ", ".join(self._succeeded))
        if self._failed:
            raise TestcasesException("FAILED to {}.".format(", ".join(self._failed)))

        logger.info("DONE - RECORDS SUCCESSFULLY UPDATED!")

    def submit_filtered_xmls(self):
        """Submits filtered XMLs to Polarion Importers."""
        if self.args.no_submit:
            return

        # update existing testcases in new thread
        output = []
        updating_testcases_t = None
        if not self.args.no_testcases_update and self.filtered_xmls.updated_testcases is not None:
            updating_testcases_t, output = self.update_existing_testcases()

        # create missing testcases in Polarion
        missing_testcases_submitted = False
        if self.filtered_xmls.missing_testcases is not None:
            missing_testcases_submitted = self.create_missing_testcases()
            self._append_msg(missing_testcases_submitted, "add missing testcases")

        # add missing testcases to testrun
        if (
            missing_testcases_submitted
            and self.args.testrun_id
            and self.filtered_xmls.missing_testsuites is not None
        ):
            missing_testcases_added = self.add_missing_testcases_to_testrun()
            self._append_msg(missing_testcases_added, "update testrun")
        elif not self.args.testrun_id:
            logger.warning("Not updating testrun, testrun ID not specified.")

        # wait for update of existing testcases to finish
        if updating_testcases_t:
            updating_testcases_t.join()
            self._append_msg(output.pop(), "update existing testcases")

        self._log_outcome()


def submit_filtered_xmls(args, submit_args, config, filtered_xmls):
    """Submits filtered XMLs to Polarion Importers."""
    return TestcasesSubmitter(args, submit_args, config, filtered_xmls).submit_filtered_xmls()


def get_testsuites_xml_root(args, config, testsuites, testsuites_transform_func=None):
    """Returns content of XML files for importers."""
    testsuites_str = gen_xmls.gen_testsuites_xml_str(
        testsuites,
        args.testrun_id or "IMPORT_{:%Y%m%d%H%M%S}".format(datetime.datetime.now()),
        config,
        testsuites_transform_func,
    )
    testsuites_root = d2p_utils.get_xml_root_from_str(testsuites_str)

    return testsuites_root


def get_testcases_xml_root(config, requirements_mapping, testcases, testcases_transform_func=None):
    """Returns content of XML files for importers."""
    testcases_str = gen_xmls.gen_testcases_xml_str(
        testcases, requirements_mapping, config, testcases_transform_func
    )
    testcases_root = d2p_utils.get_xml_root_from_str(testcases_str)

    return testcases_root


def get_init_logname(args):
    """Returns filename of the message bus log file."""
    if args.job_log:
        job_log = args.job_log
    else:
        job_log = "init-job-{}.log".format(cli_utils.get_filename_str(args))
        job_log = os.path.join(args.output_dir or "", job_log)
    return job_log


def initial_submit(args, submit_args, config, testsuites_root, log):
    """Submits XML to Polarion and saves the log file returned by the message bus."""
    if args.use_svn and not args.testrun_init:
        # no need to submit, SVN is used to generate list of missing testcases
        return
    elif os.path.isfile(log) and not args.testrun_init:
        # log file already exists, no need to generate one
        return
    elif args.no_submit:
        raise NothingToDoException(
            "Instructed not to submit and as the import log is missing, "
            "there's nothing more to do"
        )
    elif args.testrun_init and not args.testrun_id:
        raise TestcasesException("Cannot init testrun, testrun ID not specified.")
    elif testsuites_root is None:
        raise TestcasesException("Cannot init testrun, testsuites XML not generated.")

    if args.testrun_init:
        # we want to init new test run
        xml_root = testsuites_root
        if args.testrun_title:
            properties.xunit_fill_testrun_title(xml_root, args.testrun_title)
    else:
        # we want to just get the log file without changing anything
        xml_root = testsuites_root
        properties.set_dry_run(xml_root)

    properties.remove_response_property(xml_root)

    if args.output_dir:
        init_file = cli_utils.get_import_file_name(
            args, consts.TEST_RUN_XML, args.output_dir, "init"
        )
        d2p_utils.write_xml_root(xml_root, init_file)

    if not submit.submit_and_verify(xml_root=xml_root, config=config, log_file=log, **submit_args):
        raise TestcasesException("Failed to do the initial submit.")
