from fixture.application import Application
import pytest
import json
import os.path


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


# fixture for web
@pytest.fixture
def app(request):
    global fixture
    # get name browser(str) from cmd option (marker --browser)
    browser = request.config.getoption("--browser")
    # get data from json file (path to file getting from cmd option, marker --target)
    web_config = load_config(request.config.getoption("--target"))["web"]
    # validation fixture
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseUrl"])
    # fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture


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
