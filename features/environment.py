# https://behave.readthedocs.io/en/stable/tutorial.html#environmental-controls
# https://behave.readthedocs.io/en/stable/api.html#behave.runner.Context
# from behave import fixture, use_fixture
import _thread
import logging
import os
import webbrowser
from pathlib import Path

import kdb
from behave import use_step_matcher
from kdb import FolderSettings, init_folder_config_structure, report
from kdb.common.mobile_manager import MobileManager
from kdb.common.profiles import Profiles
from kdb.common.utils import FileUtil
from kdb.config.settings import refresh_settings
from kdb.report.report_manager import ReportManager
from kdb.report.test_case_log import TestCaseLog
from kdb.webdriver import kdb_driver

from conftest import check_and_create_build_lock_file

# -- SELECT DEFAULT STEP MATCHER: Use "re" matcher as default.
# use_step_matcher("cfparse")
# use_step_matcher("re")
use_step_matcher("parse")


def before_step(context, step):
    """These run before every step."""
    report.add_comment(f">>> Line {step.line}: {step.keyword} {step.name}")


def after_step(context, step):
    """These run after every step."""
    pass


def before_scenario(context, scenario):
    """These run before each scenario is run."""
    TestCaseLog.reset()
    # context.config.userdata[scenario.name + '_start_time'] = int(round(time.time() * 1000))


def after_scenario(context, scenario):
    """These run after each scenario is run."""
    # create testcase report
    # test_duration = int(round(time.time() * 1000)) - context.config.userdata.get(scenario.name + '_start_time')
    if not context.config.userdata.get("no-report"):
        # add trace log record if failed/assert fail
        if context.failed and context.stderr_capture is not None:
            TestCaseLog.add_test_step('', {}, 0, 'trace', context.stderr_capture.getvalue())
        # generate html file
        _thread.start_new_thread(ReportManager.create_test_case_report, (
            scenario.name, not context.failed, int(scenario.duration * 1000), scenario.filename))
    # print duration and status
    logging.info(f'=======Result===={scenario.name}===')
    logging.info("Testing duration: %s ms" % str(int(scenario.duration * 1000)))
    if not context.failed:
        logging.info("Testing result: %s" % 'PASSED')
    else:
        logging.info("Testing result: %s" % 'FAILURES')


def before_feature(context, feature):
    """These run before each feature file is exercised."""
    context.profile = Profiles(kdb.PROFILE_NAME)


def after_feature(context, feature):
    """These run after each feature file is exercised."""
    context.config.junit_directory = FolderSettings.XML_REPORT_DIR
    # set xml_report_name in userdata that using in after_all hook
    # feature_name = os.path.splitext(os.path.basename(feature.filename))[0]
    feature_name = os.path.splitext(feature.filename)[0]
    feature_name = feature_name.replace('/', '.').replace('features.', '')
    xml_fname = 'TESTS-' + feature_name + '.xml'
    context.config.userdata.xml_report_name = xml_fname


def before_all(context):
    """These run before the whole shooting match."""
    logging.info("Setting up...")
    userdata = context.config.userdata

    # init_folder_config_structure()
    PROJECT_PATH = Path(__file__).resolve(strict=True).parent.parent
    init_folder_config_structure(PROJECT_PATH)
    refresh_settings()

    # remove old output folder
    _thread.start_new_thread(FileUtil.delete_dir_and_contents_recursively,
                             (Path(FolderSettings.HTML_REPORT_DIR).parent, 3))
    _thread.start_new_thread(FileUtil.delete_dir_and_contents_recursively,
                             (Path(FolderSettings.XML_REPORT_DIR).parent, 3))
    _thread.start_new_thread(FileUtil.delete_dir_and_contents_recursively,
                             (Path(FolderSettings.DATA_REPORT_DIR).parent, 3))

    # update env variable
    # kdb.ENV = session.config.getoption("--env")
    kdb.ENV = userdata.get("env", "dev")
    # browser name is inputted in cmd
    # kdb.BROWSER = session.config.getoption("--browser")
    _browser = userdata.get("browser", "chrome")
    if _browser:
        kdb.BROWSER = _browser
    # the param values is inputted in cmd
    # parameters = session.config.getoption("--params")
    _parameters = userdata.get("params")
    if _parameters:
        kdb.PARAMS = str(_parameters).split(",")
    # The CI workspace
    # kdb.WORKSPACE = session.config.getoption("--workspace")
    _workspace = userdata.get("workspace")
    if _workspace:
        kdb.WORKSPACE = _workspace
    # create build lock file
    if kdb.WORKSPACE:
        check_and_create_build_lock_file()
    #
    _profile_name = userdata.get("profile")
    if _profile_name:
        kdb.PROFILE_NAME = _profile_name
    #
    _app_path = userdata.get("app-path")
    if _app_path:
        kdb.APP_PATH = _app_path

    # create logs folder if not exists
    if not os.path.exists(FolderSettings.LOG_DIR):
        os.makedirs(FolderSettings.LOG_DIR, exist_ok=True)
    # create html folder if not exists
    if not userdata.get("no-report") and not os.path.exists(FolderSettings.HTML_REPORT_DIR):
        os.makedirs(FolderSettings.HTML_REPORT_DIR, exist_ok=True)
    logging.info("Set up successfully")


def after_all(context):
    """These run after the whole shooting match."""
    logging.info(context.config.userdata.xml_report_name)
    logging.info('start after_all(context)')
    userdata = context.config.userdata

    # pytest_sessionfinish
    # close all browser and terminal web driver
    kdb_driver.quit()
    # close appium server port if opened
    MobileManager.close_mobile_port()

    # pytest_terminal_summary
    # copy the data/resources to CI workspace
    if kdb.WORKSPACE:
        _thread.start_new_thread(FileUtil.copytree, (FolderSettings.DATA_REPORT_DIR, kdb.WORKSPACE))
    # generate and open html report file in browser
    if not userdata.get("no-report"):
        # feature_name = os.path.splitext(os.path.basename(context.feature.filename))[0]
        # xml_fname = 'TESTS-' + feature_name + '.xml'
        xml_fname = context.config.userdata.xml_report_name
        # generate report
        html_file_path = ReportManager.create_index_report(xml_fname)
        # open report file in browser when run test on local (that means, the kdb.WORKSPACE is None)
        if html_file_path is not None:
            logging.info('The HTML report are generated!')
            if not kdb.WORKSPACE:
                webbrowser.open_new(html_file_path)
            else:
                # copy the html report to CI workspace
                logging.info(
                    '>>> Copying the HTML report to CI workspace from %s to %s.' % (
                    FolderSettings.HTML_REPORT_DIR, kdb.WORKSPACE))
                FileUtil.copytree(FolderSettings.HTML_REPORT_DIR, kdb.WORKSPACE)
