# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate


class TestGoogleLogin(StaticLiveServerTestCase):

    fixtures = ['allauth_fixture']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        # WebDriverWait is used to make the browser wait a certain
        # amount of time before rising an exception when an
        # element is not found.
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')

    def tearDown(self):
        self.browser.quit()

    # get_element_by_id and get_button_by_id are helper functions that use
    # WebDriverWait to find elements by ID. Note that for a button we
    # wait until the element is clickable.

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
                                      (By.ID, element_id)))

    # test for password

    def get_element_by_name(self, element_name):
        return self.browser.wait.until(EC.presence_of_element_located(
                                      (By.NAME, element_name)))

    def get_element_by_xpath(self, element_name):
        return self.browser.wait.until(EC.element_to_be_clickable(
                                      (By.XPATH, element_name)))

    def get_element_by_(self, element_name):
        return self.browser.wait.until(EC.presence_of_element_located(
                                      (By.NAME, element_name)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
                                      (By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def user_login(self):
        import json
        with open("taskbuster/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        self.get_element_by_id("identifierId").send_keys(credentials["Email"])
        self.get_button_by_id("identifierNext").click()
        # browser.find_element_by_name("password").send_keys(credentials["Passwd"])
        self.get_element_by_xpath("//input[@name='password']").send_keys(
            credentials["Passwd"])
        for btn in ["signin", "submit_approve_access"]:
            self.get_button_by_id("passwordNext").click()
        return

        # test_google_login is the main test here. It goes to the
        # home page and:
        # checks that the login button is present
        # checks that the logout button is not present
        # checks that the login button points to the correct
        # url (/accounts/google/login)
        # checks that after clicking on the login button, the user gets logged
        # in and it sees the logout button instead.
        # a click on the logout button should make the user see the login
        # button again.

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        # It is also possible to check that exceptions and warnings
        # are raised using the following methods ->assertRaises
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        google_login.click()
        self.user_login()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")
