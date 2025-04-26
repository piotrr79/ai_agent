# tests/views_tests.py
from django.test import TestCase
from django.urls import reverse
from ..views.homeView import HomeView


class ViewsTests(TestCase):
    """ ValidatorTests class """

    def test_home_page(self):
        """ Test home page response

            Returns:
                None
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        """ Test home page response by url name

            Returns:
                None
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)