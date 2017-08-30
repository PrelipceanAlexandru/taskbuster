# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from datetime import date
from django.utils import formats
from django.utils.translation import activate

import unittest
import warnings


class HomeNewVisitorTest(StaticLiveServerTestCase):
    # open teh brouser  and wait 3 seconds if needs to

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        activate('en')
    # close the browser

    def tearDown(self):
        self.browser.quit()
    # takes one argument "namespace"

    def get_full_url(self, namespace):
        # live_server_url -> gives you the local host url
        # reverse(namespace) -> gives you the relative url of a given
        # namespace "/"
        # return -> http://127.0.0.1:8000/
        return self.live_server_url + reverse(namespace)

    # assert that the title of the page has Welcome to Django
    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn('Welcome to TaskBuster!', self.browser.title)

    # def test_h1_css(self):
    #     self.browser.get(self.get_full_url("home"))
    #     h1 = self.browser.find_element_by_tag_name("h1")
    #     # import ipdb; ipdb.set_trace()
    #     self.assertEqual(h1.value_of_css_property("color"),
    #                      u"rgb(200, 50, 255)")

    def test_home_files(self):
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title)

    def test_uses_index_template(self):
        activate('en')
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "taskbuster/index.html")

    def test_internationalization(self):
        for lang, h1_text in [('en', 'Welcome to TaskBuster!'),
                              ('ca', 'Benvingut a TaskBuster!')]:
            activate(lang)
            self.browser.get(self.get_full_url("home"))
            h1 = self.browser.find_element_by_tag_name("h1")
            self.assertEqual(h1.text, h1_text)

    def test_localization(self):
        today = date.today()
        for lang in ['en', 'ca']:
            activate(lang)
            self.browser.get(self.get_full_url("home"))
            local_date = self.browser.find_element_by_id("local-date")
            non_local_date = self.browser.find_element_by_id("non-local-date")
            self.assertEqual(formats.date_format(today, use_l10n=True),
                             local_date.text)
            self.assertEqual(today.strftime('%Y-%m-%d'), non_local_date.text)

    def test_time_zone(self):
        self.browser.get(self.get_full_url("home"))
        tz = self.browser.find_element_by_id("time-tz").text
        utc = self.browser.find_element_by_id("time-utc").text
        ny = self.browser.find_element_by_id("time-ny").text
        self.assertNotEqual(tz, utc)
        self.assertNotIn(ny, [tz, utc])


if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    with warnings.catch_warnings(record=True):
        unittest.main()
