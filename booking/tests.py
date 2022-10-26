from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class BookingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_room(self):
        data = {"capacity": 10}
        response = self.client.post('/rooms/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event(self):
        data = {
            "title": "Titulo del evento",
            "room": 1,
            "date": "2022-10-10"
        }
        response = self.client.post('/events/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

