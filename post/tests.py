from django.test import TestCase
from .models import Post, Vote, Competition
from post.views import post_list
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response


class PostTests(TestCase):
    """
    Here we'll define the tests
    that we'll run against our Post model
    """

    #def test_str(self):
     #   test_title = Post(title='Testing the title')
      #  self.assertEqual(str(test_title),
       #                  'the title')

    def test_str_post(self):
        test_title = Post(title='Testing the title')
        self.assertEqual(str(test_title),
                         'Testing the title')

    def test_str_comp(self):
        test_title = Competition(title='Testing the title')
        self.assertEqual(str(test_title),
                         'Testing the title')




class PostListTests(TestCase):
    def test_post_list_page_resolves(self):
        list_page = resolve('/posts/')
        self.assertEqual(list_page.func, post_list)

    def test_post_list_page_status_code(self):
        list_page = self.client.get('/posts/')
        self.assertEqual(list_page.status_code, 200)

    def test_check_content_is_correct(self):
        about_page = self.client.get('/posts/')
        self.assertTemplateUsed(about_page, "posts/postlist.html")
        list_page_template_output = render_to_response("posts/postlist.html").content
        self.assertEqual(about_page.content, list_page_template_output)


