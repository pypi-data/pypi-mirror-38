# -*- coding: utf-8 -*-
"""
Main CLI.
"""

from __future__ import absolute_import, unicode_literals

import argparse
import logging

from cfme_testcases import (
    cli_requirements,
    cli_testcases,
    cli_utils,
    collect,
    configuration,
    filters,
    missing,
)
from cfme_testcases.exceptions import Dump2PolarionException, NothingToDoException
from dump2polarion import utils as d2p_utils

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


def get_args(args=None):
    """Get command line arguments."""
    parser = argparse.ArgumentParser(description="cfme-testcases")
    parser.add_argument("-t", "--testrun-id", help="Polarion test run id")
    parser.add_argument("-o", "--output_dir", help="Directory for saving generated XML files")
    parser.add_argument(
        "-n", "--no-submit", action="store_true", help="Don't submit generated XML files"
    )
    parser.add_argument(
        "--testrun-init", action="store_true", help="Create and initialize new testrun"
    )
    parser.add_argument("--testrun-title", help="Title to set for the new testrun")
    parser.add_argument(
        "--data-in-code",
        action="store_true",
        help="Source code is an authoritative source of data.",
    )
    parser.add_argument("--user", help="Username to use to submit to Polarion")
    parser.add_argument("--password", help="Password to use to submit to Polarion")
    parser.add_argument("--testcases", help="Path to JSON file with testcases")
    parser.add_argument("--testsuites", help="Path to JSON file with testsuites")
    parser.add_argument("--config", help="Path to polarion_tools config YAML")
    parser.add_argument("--job-log", help="Path to an existing job log file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, don't update anything")
    parser.add_argument("--no-requirements", action="store_true", help="Don't import requirements")
    parser.add_argument(
        "--no-testcases-update", action="store_true", help="Don't update existing testcases"
    )
    parser.add_argument("--no-verify", action="store_true", help="Don't verify import success")
    parser.add_argument(
        "--verify-timeout",
        type=int,
        default=600,
        metavar="SEC",
        help="How long to wait (in seconds) for verification of submission success"
        " (default: %(default)s)",
    )
    parser.add_argument(
        "--use-svn", metavar="SVN_REPO", help="Path to SVN repo with Polarion project"
    )
    parser.add_argument("--log-level", help="Set logging to specified level")
    return parser.parse_args(args)


# pylint: disable=too-many-locals,too-many-arguments
def update_testcases(
    args,
    config,
    requirements_data=None,
    requirements_transform_func=None,
    testsuites_transform_func=None,
    testcases_transform_func=None,
):
    """Testcases update main function."""
    assert isinstance(requirements_data, list) if requirements_data is not None else True

    submit_args = cli_utils.get_submit_args(args)

    try:
        __, testcases_json, testsuites_json = collect.collect_testcases(
            config.get("pytest_collect"),
            args.testcases,
            args.testsuites,
            testsuites_needed=cli_utils.is_testsuites_xml_needed(args),
        )

        requirements_root = None
        requirements_mapping = None

        if not args.no_requirements:
            requirements_root = cli_requirements.get_requirements_xml_root(
                config,
                testcases_json,
                requirements_data=requirements_data,
                transform_func=requirements_transform_func,
            )
            requirements_mapping = cli_requirements.get_requirements_mapping(
                args, submit_args, config, requirements_root
            )

        if testsuites_json:
            testsuites_root = cli_testcases.get_testsuites_xml_root(
                args, config, testsuites_json, testsuites_transform_func
            )
        testcases_root = cli_testcases.get_testcases_xml_root(
            config, requirements_mapping, testcases_json, testcases_transform_func
        )

        init_logname = cli_testcases.get_init_logname(args)
        cli_testcases.initial_submit(args, submit_args, config, testsuites_root, init_logname)

        missing_testcases = missing.get_missing(config, testcases_root, init_logname, args.use_svn)
        filtered_xmls = filters.get_filtered_xmls(
            testcases_root,
            testsuites_root if args.testrun_id else None,
            missing_testcases,
            data_in_code=args.data_in_code,
        )

        cli_utils.save_generated_xmls(args, filtered_xmls, requirements_root)
        cli_testcases.submit_filtered_xmls(args, submit_args, config, filtered_xmls)
    except NothingToDoException as einfo:
        logger.info(einfo)
        return 0
    except Dump2PolarionException as err:
        logger.fatal(err)
        return 1
    return 0


def main(
    args=None,
    requirements_transform_func=None,
    testsuites_transform_func=None,
    testcases_transform_func=None,
):
    """Main function for CLI."""
    args = get_args(args)
    d2p_utils.init_log(args.log_level)
    config = configuration.get_config(args.config)

    return update_testcases(
        args,
        config,
        requirements_transform_func=requirements_transform_func,
        testsuites_transform_func=testsuites_transform_func,
        testcases_transform_func=testcases_transform_func,
    )
