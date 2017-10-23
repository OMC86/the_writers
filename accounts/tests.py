# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from accounts.views import landing
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
# Create your tests here.


class LandingPageTest(TestCase):

    def test_landing_page_resolves(self):
        landing_page = resolve('')
        self.assertEqual(landing_page.func, landing)

    def test_landing_page_status_code(self):
        landing_page = self.client.get('')
        self.assertEqual(landing_page.status_code, 200)

    def test_check_landing_content_is_correct(self):
        landing_page = self.client.get('')
        self.assertTemplateUsed(landing_page, "landing.html")
        landing_page_template_output = render_to_response("landing.html").content
        self.assertEqual(landing_page.content, landing_page_template_output)
