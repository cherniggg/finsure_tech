import csv
import os

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Lender

class LenderTests(APITestCase):
    def setUp(self):
        Lender.objects.create(
            name="test",
            code="123",
            trial_commission_rate=92,
            upfront_commission_rate=22,
            active=False
        )

    def test_create_lender(self):

        url = reverse('lender-list')
        data = {
            "data": {
                "type": "Lender",
                "attributes": {
                    "name": "Test User",
                    "code": "asf",
                    "trial_commission_rate": 99,
                    "active": True,
                    "upfront_commission_rate": 22
                }
            }
        }
        response = self.client.post(url, data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lender.objects.count(), 2)
        self.assertEqual(Lender.objects.last().name, 'Test User')
    
    def test_update_lender(self):

        obj_id = Lender.objects.first().pk
        url = reverse('lender-list') + f'{obj_id}/'
        data = {
            "data": {
                "type": "Lender",
                "id": obj_id,
                "attributes": {
                    "code": "aaa",
                }
            }
        }
        response = self.client.patch(url, data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lender.objects.first().code, 'aaa')
    
    def test_csv_upload(self):
        
        csv_file = open(os.path.join(settings.PROJECT_ROOT, 'lenders.csv'))
        url = reverse('lender-csv')
        response = self.client.post(url, {'csv_file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lender.objects.last().code, 'abc')
        self.assertEqual(Lender.objects.count(), 4)
    
    def test_csv_download(self):
        
        url = reverse('lender-csv')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)