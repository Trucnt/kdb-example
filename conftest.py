import _thread
import csv
import logging
import os
import random
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import kdb
import pytest
from _pytest.junitxml import LogXML
from kdb import FolderSettings, XML_REPORT_FILE, init_folder_config_structure
from kdb.common.mobile_manager import MobileManager
from kdb.common.profiles import Profiles
from kdb.common.utils import FileUtil
from kdb.config.settings import IESettings, refresh_settings
from kdb.report.report_manager import ReportManager
from kdb.report.test_case_log import TestCaseLog
from kdb.webdriver import kdb_driver


@pytest.fixture(scope="session")
def params(request):
    """
    Read the parameters from cmd
    """
    yield kdb.PARAMS


@pytest.fixture(scope="session")
def profile(request):
    """
    Load profile with name from cmd
    """
    profile = Profiles(kdb.PROFILE_NAME)
    yield profile


@pytest.fixture(scope="session")
def data_test(request):
    """
    Read the data test that inputted in cmd
    """
    logging.info("Reading the data test file...")
    # the data test path is inputted in cmd
    data_path_cmd = request.config.getoption("--data-test")
    logging.info(">>> The data test path inputted: " + str(data_path_cmd))
    data_test_path = FileUtil.get_absolute_path(data_path_cmd)
    logging.info(">>> Get full path of the data test file: " + str(data_test_path))
    data_test_file = None
    reader = []
    if data_test_path and os.path.isfile(data_test_path):
        # open data test file
        data_test_file = open(data_test_path, encoding="utf8")
        reader = csv.DictReader(data_test_file, delimiter='\t')
        logging.info(">>> Read the data test successfully.")
    else:
        args = request.config.args
        if args and len(args) > 0 and os.path.isfile(args[0]):
            data_test_file_name = os.path.splitext(os.path.basename(args[0]))[0] + '.csv'
            data_test_path = FileUtil.get_absolute_path(data_test_file_name)
            logging.info(">>> Get full path of the data test file (2): " + str(data_test_path))
            if data_test_path and os.path.isfile(data_test_path):
                # open data test file
                data_test_file = open(data_test_path, encoding="utf8")
                reader = csv.DictReader(data_test_file, delimiter='\t')
                logging.info(">>> Read the data test successfully. (2)")
            else:
                logging.warning(">>> The data test file is not exists or cannot readable. (2)")
        else:
            logging.warning(">>> The data test file is not exists or cannot readable.")
    yield reader
    # close date test file if opened
    if data_test_file and not data_test_file.closed:
        data_test_file.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    logging.info("start pytest_runtest_makereport")
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def testcase_report_generation(request):
    logging.info("start testcase_report_generation")
    name = request.node.name
    # reset TestCaseLog
    TestCaseLog.reset()

    start_time = int(round(time.time() * 1000))
    yield
    test_duration = int(round(time.time() * 1000)) - start_time
    if not request.config.getoption("--no-report"):
        # add trace log record if failed/assert fail
        if request.node.rep_call.failed:
            TestCaseLog.add_test_step('', {}, 0, 'trace', request.node.rep_call.longreprtext)
        # generate html file
        _thread.start_new_thread(ReportManager.create_test_case_report, (
            name, request.node.rep_call.passed and TestCaseLog.passed(), test_duration, request.node.nodeid))
    # print duration and status
    logging.info('=======Result=======')
    logging.info("Testing duration: %s ms" % str(test_duration))
    if request.node.rep_call.passed and TestCaseLog.passed():
        logging.info("Testing result: %s" % 'PASSED')
    else:
        logging.info("Testing result: %s" % 'FAILURES')


def pytest_addoption(parser):
    logging.info("start pytest_addoption")
    parser.addoption("--no-report", action="store_true", default=False,
                     help="do not show html report after test completely if it's true")
    parser.addoption("--env", default="production", help="environment testing: produdtion, ect")
    # nargs='?' means 0-or-1 arguments
    # const="chrome" sets the default when there are 0 arguments
    parser.addoption("--browser", nargs='?', const="chrome", default="chrome", help="browser default for testing")
    parser.addoption("--params", nargs='?', const=None, help="The param values are inputted via cmd")
    parser.addoption("--data-test", nargs='?', const=None, help="The data test path inputted via cmd")
    # workspace
    parser.addoption("--workspace", nargs='?', const=None, help="The CI workspace")
    #
    parser.addoption("--app-path", nargs='?', const=None, help="The .apk/.ipa file path")
    parser.addoption("--profile", nargs='?', const=None, help="The name of profile without extension (.profile)")


def pytest_configure(config):
    logging.info("start pytest_configure")
    # Set xml report
    # if not config.option.xmlpath and not hasattr(config, 'slaveinput'):
    if not hasattr(config, 'slaveinput'):
        xmlpath = os.path.join(FolderSettings.XML_REPORT_DIR, XML_REPORT_FILE)
        config._xml = LogXML(xmlpath, config.option.junitprefix, config.getini('junit_suite_name'))
        config.pluginmanager.register(config._xml)


def pytest_sessionstart(session):
    logging.info("Setting up...")
    # init_folder_config_structure()
    PROJECT_PATH = Path(__file__).resolve(strict=True).parent
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
    kdb.ENV = session.config.getoption("--env")
    # browser name is inputted in cmd
    _browser = session.config.getoption("--browser")
    if _browser is not None:
        kdb.BROWSER = _browser
    # the param values is inputted in cmd
    _parameters = session.config.getoption("--params")
    if _parameters:
        kdb.PARAMS = str(_parameters).split(",")
    # The CI workspace
    _workspace = session.config.getoption("--workspace")
    if _workspace is not None:
        kdb.WORKSPACE = _workspace
    # create build lock file
    if kdb.WORKSPACE:
        check_and_create_build_lock_file()
    #
    _profile = session.config.getoption("--profile")
    if _profile is not None:
        kdb.PROFILE_NAME = _profile
    #
    _app_path = session.config.getoption("--app-path")
    if _app_path is not None:
        kdb.APP_PATH = _app_path

    # create logs folder if not exists
    if not os.path.exists(FolderSettings.LOG_DIR):
        os.makedirs(FolderSettings.LOG_DIR, exist_ok=True)
    # create html folder if not exists
    if not session.config.getoption("--no-report") and not os.path.exists(FolderSettings.HTML_REPORT_DIR):
        os.makedirs(FolderSettings.HTML_REPORT_DIR, exist_ok=True)
    logging.info("Set up successfully")


def check_and_create_build_lock_file():
    logging.info("start check_and_create_build_lock_file")
    date_fmt = '%Y-%m-%d %H:%M:%S.%f'
    build_lock_file = os.path.join(kdb.WORKSPACE, kdb.BUILD_LOCK_FILE)
    # force delete the BUILD_LOCK_FILE file if file is created more than 1 hours
    if os.path.exists(build_lock_file) and os.path.isfile(build_lock_file):
        # read date time in BUILD_LOCK_FILE file
        with open(build_lock_file) as bfile:
            date_str = bfile.readline()
            if date_str == '':
                past_time = datetime.fromtimestamp(os.path.getmtime(build_lock_file))
            else:
                past_time = datetime.strptime(date_str, date_fmt)
        # log this job has other build is running warning
        logging.warning(' >>> This job has other build is running (started at %s). This build will be '
                        'wait for that the other running build is done.' % past_time.strftime(date_fmt))
        # force delete the BUILD_LOCK_FILE file if file is created more than 1 hours
        show_hint = True
        while True:
            # check timeout
            # force delete the BUILD_LOCK_FILE file and break if file is created more than 1 hours
            if (datetime.strptime(datetime.today().strftime(date_fmt), date_fmt) - past_time).days > 0 or (
                    datetime.strptime(datetime.today().strftime(date_fmt), date_fmt) - past_time).seconds > 3600:
                # delete the BUILD_LOCK_FILE file
                os.remove(build_lock_file)
                logging.info('>>> Force delete the BUILD_LOCK_FILE file and continuous this build '
                             'because the other running build is started more than 1 hours ago.')
                break
            # break if the lock file is removed by previous job
            if not os.path.exists(build_lock_file):
                logging.info(">>> The other running build has done. Let's continuous!")
                break
            # show warning if the lock file is created more than 10 minutes
            if (datetime.strptime(datetime.today().strftime(date_fmt), date_fmt) - past_time).days > 0 or (
                    datetime.strptime(datetime.today().strftime(date_fmt), date_fmt) - past_time).seconds > (10 * 60):
                if show_hint:
                    logging.warning(' >>> The other running build is started  more than 10 minutes ago.')
                    logging.warning(' >>> Please check this job that if no any other build is running, we could '
                                    'delete manually the %s in its workspace or it will be automate delete '
                                    'after 1 (one) hours. <<<' % kdb.BUILD_LOCK_FILE)
                    logging.info('>>> Please wait until the other running build done if it still running.')
                    # only show hint one times
                    show_hint = False
        # sleep a bit to avoid many build start the same time
        time.sleep(random.randint(1, 100) / 100)
        # make sure that the BUILD_LOCK_FILE don't created by other build.
        if os.path.exists(build_lock_file) and os.path.isfile(build_lock_file):
            logging.info('>>> Oh! There is another build that has just begun.')
            check_and_create_build_lock_file()
    # create BUILD_LOCK_FILE file and insert current datetime
    with open(build_lock_file, 'w+') as bfile:
        bfile.write(datetime.today().strftime(date_fmt))


def pytest_sessionfinish(session, exitstatus):
    logging.info('start pytest_sessionfinish')
    # close all browser and terminal web driver
    kdb_driver.quit()
    # close appium server port if opened
    MobileManager.close_mobile_port()


def pytest_runtest_teardown(item, nextitem):
    logging.info('start pytest_runtest_teardown')
    # quit driver if test fail
    if item.rep_call.failed:
        kdb_driver.quit()
        FileUtil.remove_file(IESettings.IE_LOG_FILE)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    logging.info('start pytest_terminal_summary')
    # copy the data/resources to CI workspace
    if kdb.WORKSPACE:
        _thread.start_new_thread(FileUtil.copytree, (FolderSettings.DATA_REPORT_DIR, kdb.WORKSPACE))
    # generate and open html report file in browser
    if not terminalreporter.config.getoption("--no-report"):
        # generate report
        html_file_path = ReportManager.create_index_report()
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
