from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper


class Application:
    """Test class for initializing and drop object"""

    def __init__(self, browser, config):
        # choice browser driver
        if browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "ie":
            self.driver = webdriver.Ie()
        else:
            raise ValueError(f"Unrecognized browser {browser}")
        self.vars = {}
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.base_url = config["web"]["baseUrl"]
        self.config = config

    def open_home_page(self):
        self.driver.get(self.base_url)
        self.driver.set_window_size(1012, 691)

    def is_valid(self):
        try:
            assert self.driver.current_url
            return True
        except:
            return False

    def destroy(self):
        self.driver.quit()
