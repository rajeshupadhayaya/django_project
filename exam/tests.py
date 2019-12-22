from django.urls import reverse, resolve
from django.test import TestCase
from .models import ExamCreateDetails
from .views import IndexView
# Create your tests here.


class HomeTests(TestCase):
    def setup(self):
        ExamCreateDetails.objects.create(username='test')
    def test_home_view_status_code(self):
        url = reverse('onlineexam:index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
