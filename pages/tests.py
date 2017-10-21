# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from pages.views import about
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
# Create your tests here.

class AboutPageTest(TestCase):
    # this test will fail
    # def test_about_page_resolves(self):
    #   about_page = resolve('')
    #   self.assertEqual(about_page.func, about)

    def test_about_page_resolves(self):
        about_page = resolve('/pages/about/')
        self.assertEqual(about_page.func, about)

    def test_about_page_status_code(self):
        about_page = self.client.get('/pages/about/')
        self.assertEqual(about_page.status_code, 200)

    def test_check_content_is_correct(self):
        about_page = self.client.get('/pages/about/')
        self.assertTemplateUsed(about_page, "about.html")
        about_page_template_output = render_to_response("about.html").content
        self.assertEqual(about_page.content, about_page_template_output)

