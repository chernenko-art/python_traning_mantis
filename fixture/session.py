from selenium.webdriver.common.by import By


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        self.app.open_home_page()
        self.app.driver.find_element(By.NAME, "username").click()
        self.app.driver.find_element(By.NAME, "username").clear()
        self.app.driver.find_element(By.NAME, "username").send_keys(username)
        self.app.driver.find_element(By.NAME, "password").click()
        self.app.driver.find_element(By.NAME, "password").clear()
        self.app.driver.find_element(By.NAME, "password").send_keys(password)
        self.app.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    def ensure_login(self, username, password):
        if self.is_loggined() > 0:
            if self.check_loggined_name() != username:
                self.logout()
            else:
                return
        self.login(username, password)

    def check_loggined_name(self):
        return self.app.driver.find_element(By.CSS_SELECTOR, "td.login-info-left span").text

    def is_loggined_in_as(self, name):
        return self.check_loggined_name() == name

    def is_loggined(self):
        return len(self.app.driver.find_elements(By.LINK_TEXT, "Logout"))

    def logout(self):
        self.app.driver.find_element(By.LINK_TEXT, "Logout").click()
