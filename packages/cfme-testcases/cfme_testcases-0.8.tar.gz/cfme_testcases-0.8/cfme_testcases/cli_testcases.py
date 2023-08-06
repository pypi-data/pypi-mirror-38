# -*- coding: utf-8 -*-
"""
Create new testrun and upload missing testcases using Polarion Importers.
"""

from __future__ import absolute_import, unicode_literals

import logging

from cfme_testcases import consts, testcases_submit, utils
from cfme_testcases.exceptions import NothingToDoException, TestcasesException
from dump2polarion import properties, submit
from dump2polarion import utils as d2p_utils

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


def _append_msg(retval, msg, succeeded, failed):
    if retval:
        succeeded.append(msg)
    else:
        failed.append(msg)


def _log_outcome(succeeded, failed):
    if succeeded and failed:
        logger.info("SUCCEEDED to %s", ", ".join(succeeded))
    if failed:
        raise TestcasesException("FAILED to {}.".format(", ".join(failed)))

    logger.info("DONE - RECORDS SUCCESSFULLY UPDATED!")


# pylint: disable=too-many-arguments
def _import_missing(args, submit_args, config, filtered_xmls, succeeded, failed):
    # create missing testcases in Polarion
    testcases_submitted = False
    try:
        testcases_submitted = testcases_submit.create_missing_testcases(
            submit_args, config, filtered_xmls, output_dir=args.output_dir
        )
        _append_msg(testcases_submitted, "add missing testcases", succeeded, failed)
    except NothingToDoException:
        pass

    # add missing testcases to testrun
    if testcases_submitted and args.testrun_id:
        try:
            testcases_added = testcases_submit.add_missing_testcases_to_testrun(
                submit_args, config, filtered_xmls, output_dir=args.output_dir
            )
            _append_msg(testcases_added, "update testrun", succeeded, failed)
        except NothingToDoException:
            pass
    elif not args.testrun_id:
        logger.warning("Not updating testrun, testrun ID not specified.")


def submit_filtered_xmls(args, submit_args, config, filtered_xmls):
    """Submits filtered XMLs to Polarion Importers."""
    if not submit_args:
        return

    succeeded, failed = [], []

    # update existing testcases in new thread
    updating_testcases_t = None
    if not args.no_testcases_update:
        try:
            updating_testcases_t, output = testcases_submit.update_existing_testcases(
                submit_args, config, filtered_xmls, output_dir=args.output_dir
            )
        except NothingToDoException:
            pass

    # import missing data
    _import_missing(args, submit_args, config, filtered_xmls, succeeded, failed)

    # wait for update of existing testcases to finish
    if updating_testcases_t:
        updating_testcases_t.join()
        _append_msg(output.pop(), "update existing testcases", succeeded, failed)

    _log_outcome(succeeded, failed)


def initial_submit(args, submit_args, config, testsuites_root):
    """Submits XML to Polarion and saves the log file returned by the message bus."""
    if args.use_svn and not args.testrun_init:
        # no need to submit, SVN is used to generate list of missing testcases
        return None
    elif args.no_submit:
        raise NothingToDoException(
            "Instructed not to submit and as the import log is missing, "
            "there's nothing more to do"
        )
    elif args.testrun_init and not args.testrun_id:
        raise TestcasesException("Cannot init testrun, testrun ID not specified.")
    elif testsuites_root is None:
        raise TestcasesException("Cannot init testrun, testsuites XML not generated.")

    xml_root = testsuites_root
    # we want to just get the log file without changing anything
    dry_run = True
    if args.testrun_init:
        # we want to init new test run
        dry_run = False
        if args.testrun_title:
            properties.xunit_fill_testrun_title(xml_root, args.testrun_title)

    properties.remove_response_property(xml_root)

    if args.output_dir:
        init_file = utils.get_import_file_name(consts.TEST_SUITE_XML, args.output_dir, "init")
        d2p_utils.write_xml_root(xml_root, init_file)

    log = utils.get_job_logname("init", args.output_dir)
    init_sargs = submit_args.copy()
    init_sargs["dry_run"] = dry_run
    if not submit.submit_and_verify(xml_root=xml_root, config=config, log_file=log, **init_sargs):
        raise TestcasesException("Failed to do the initial submit.")

    return log
