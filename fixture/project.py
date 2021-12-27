from model.project import Project
from selenium.webdriver.common.by import By
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_add_project_page(self):
        self.open_project_page()
        self.app.driver.find_element(By.CSS_SELECTOR, ".form-title .button-small").click()

    def open_project_page(self):
        self.app.driver.find_element(By.LINK_TEXT, "Manage").click()
        self.app.driver.find_element(By.LINK_TEXT, "Manage Projects").click()

    def get_project_list(self):
        self.open_project_page()
        project_list = []
        web_project_list = self.app.driver.find_elements(By.CSS_SELECTOR, 'table[cellspacing="1"].width100 tr')[2:]
        for project in web_project_list:
            project_params = project.find_elements(By.TAG_NAME, "td")
            string_whith_id = project_params[0].find_element(By.TAG_NAME, "a").get_attribute("href")
            id = re.search("id=(.*)", string_whith_id).group(1)
            name = project_params[0].text
            status = project_params[1].text
            view_state = project_params[3].text
            description = project_params[4].text
            project_list.append(Project(id=id, name=name, status=status, view_state=view_state, description=description))
        return project_list

    def add_project_page_is_view(self):
        page_is_view = self.app.driver.find_elements(By.XPATH, "//input[@value='Add Project']")
        return len(page_is_view) > 0

    def add_new(self, project):
        if not self.add_project_page_is_view():
            self.open_add_project_page()
        self.fill_project_form(project)
        self.click_create_project_button()
        self.go_to_home_page()

    def change_field_value(self, field_name, text):
        if text is not None:
            # check text field
            if field_name not in ["status", "view_state", "inherit_global"]:
                self.app.driver.find_element(By.NAME, field_name).click()
                self.app.driver.find_element(By.NAME, field_name).clear()
                self.app.driver.find_element(By.NAME, field_name).send_keys(text)
            # check checkbox field
            elif field_name == "inherit_global":
                if text != "True":
                    self.app.driver.find_element(By.NAME, "inherit_global").click()
            # check dropdown list
            else:
                self.app.driver.find_element(By.NAME, field_name).click()
                dropdown = self.app.driver.find_element(By.NAME, field_name)
                dropdown.find_element(By.XPATH, f"//option[. = '{text}']").click()

    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("status", project.status)
        self.change_field_value("inherit_global", project.inherit_global)
        self.change_field_value("view_state", project.view_state)
        self.change_field_value("description", project.description)

    def click_create_project_button(self):
        self.app.driver.find_element(By.XPATH, "//input[@value='Add Project']").click()

    def go_to_home_page(self):
        self.app.driver.find_element(By.CSS_SELECTOR, "body > div img").click()
