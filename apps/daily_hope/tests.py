from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import HopefulBeginningCompletion

class HopefulBeginningCompletionTests(APITestCase):
    def test_record_completion(self):
        url = reverse('hopeful_beginning_complete')
        initial_count = HopefulBeginningCompletion.objects.count()
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HopefulBeginningCompletion.objects.count(), initial_count + 1)
        self.assertEqual(response.data['message'], "Hopeful Beginning completion recorded.")
