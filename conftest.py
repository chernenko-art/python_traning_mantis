from fixture.application import Application
import pytest
import json
import os.path
import ftputil


fixture = None
target = None


# help functions for load config
def load_config(file):
    global target
    if target is None:
        # absolut path to file target.json
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        # load data from json
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


# fixture for web
@pytest.fixture
def app(request, config):
    global fixture
    # get name browser(str) from cmd option (marker --browser)
    browser = request.config.getoption("--browser")
    # validation fixture
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
        fixture.session.ensure_login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        # check exists old config file on ftp server
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        # check exists config file on ftp server
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        # upload config file on ftp server
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


#  finalizing web fixture
@pytest.fixture(scope="session", autouse=True)  # autouse - automatic start fixture
def stop(request):
    def fin():
        fixture.session.logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


# pytest hook - get params from cmd markers
def pytest_addoption(parser):
    # option for choice web browser
    parser.addoption("--browser", action="store", default="chrome")  # get value
    # option for get configuration from json file
    parser.addoption("--target", action="store", default="target.json")  # get path to json file
