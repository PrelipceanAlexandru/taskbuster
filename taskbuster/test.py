# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import activate


class TestHomePage(TestCase):

    def test_uses_index_template(self):
        # https://docs.djangoproject.com/en/1.11/topics/testing/tools/
        # https://stackoverflow.com/questions/11241668/what-is-reverse-in-django
        activate('en')
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "taskbuster/index.html")

    def test_uses_base_template(self):
        activate('en')
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")
