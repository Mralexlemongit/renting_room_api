from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class RoomsTestCase(TestCase):
    fixtures = ['booking.json', ]
    
    def setUp(self):
        self.unauthenticated = APIClient()
        self.business_client = APIClient()
        self.business_client.login(username='admin', password='admin')
        self.customer_client = APIClient()
        self.customer_client.login(username='custom', password='admin')

    def test_unauthenticated_can_list_rooms(self):
        response = self.unauthenticated.get('/cuartos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    
    def test_businnes_can_create_room(self):
        data = {"capacity": 10}
        response = self.business_client.post('/cuartos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
    
    def test_customer_cannot_create_room(self):
        data = {"capacity": 10}
        response = self.customer_client.post('/cuartos/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_unauthenticated_can_retrive_room(self):
        response = self.unauthenticated.get('/cuartos/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_unauthenticated_can_retrive_room(self):
        response = self.unauthenticated.get('/cuartos/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_update_room_is_not_allowed(self):
        data = {"capacity": 11}
        response = self.business_client.put('/cuartos/1', data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, response.data)

    def test_business_can_delete_room(self):
        response = self.business_client.delete('/cuartos/2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)

    def test_customer_cannot_delete_room(self):
        response = self.customer_client.delete('/cuartos/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)


class EventsTestCase(TestCase):
    fixtures = ['booking.json', ]
    
    def setUp(self):
        self.unauthenticated = APIClient()
        self.business_client = APIClient()
        self.business_client.login(username='admin', password='admin')
        self.customer_client = APIClient()
        self.customer_client.login(username='custom', password='admin')

    def test_unauthenticated_can_list_events(self):
        response = self.unauthenticated.get('/eventos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_businnes_can_list_private_events(self):
        response = self.business_client.get('/eventos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_business_can_create_event(self):
        data = {"title": "Titulo del evento", "room": 1, "date": "2022-10-11"}
        response = self.business_client.post('/eventos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_business_cannot_create_event_with_day_and_room_not_unique(self):
        data = {"title": "Titulo del evento", "room": 1, "date": "2022-10-10"}
        response = self.business_client.post('/eventos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_unauthenticated_can_retrive_public_event(self):
        response = self.unauthenticated.get('/eventos/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_owner_can_retrive_public_event(self):
        response = self.business_client.get('/eventos/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_owner_can_update_public_event(self):
        data = {"title": "Modificado", "room": 1, "date": "2022-10-15"}
        response = self.business_client.put('/eventos/2', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_owner_cannot_delete_public_event(self):
        data = {"title": "Modificado", "room": 1, "date": "2022-10-15"}
        response = self.business_client.delete('/eventos/2', data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, response.data)

class BookingTestCase(TestCase):
    fixtures = ['booking.json', ]
    
    def setUp(self):
        self.unauthenticated = APIClient()
        self.business_client = APIClient()
        self.business_client.login(username='admin', password='admin')
        self.customer_client = APIClient()
        self.customer_client.login(username='custom', password='admin')

    def test_customer_can_list_booking(self):
        response = self.customer_client.get('/reservaciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_can_list_booking_of_events(self):
        response = self.business_client.get('/reservaciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_can_create_bookign(self):
        data = {'event': 1,}
        response = self.customer_client.post('/reservaciones/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_customer_cannot_create_bookign_twice(self):
        data = {'event': 1,}
        response = self.business_client.post('/reservaciones/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_customer_cannot_book_full_event(self):
        data = {'event': 2}
        response = self.business_client.post('/reservaciones/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    # def test_can_cancel_and_rebook_event(self):
    #     response = self.client.delete('/reservaciones/2/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     data = {'event': 2, 'user': 1}
    #     response = self.client.post('/reservaciones/', data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    # def test_business_can_book_himself_in_private_event(self):
    # def test_business_can_book_others_in_private_event(self):
    # def test_customer_canot_book_private_event(self):
    # def test_user_can_book_event(self):
    # def test_user_cannot_book_full_event(self):
    # def test_business_can_create_room(self):
    # def test_customer_cannot_create_room(self):
    # def test_business_can_create_event(self):
    # def test_customer_cannot_create_event(self):
    # def test_businnes_can_delete_room(self):
    # def test_businnes_cannot_delete_room_with_pending_events(self):
    # def test_customer_cannot_delete_room(self):
    # def test_customer_can_see_available_public_events(self):
    # def test_business_can_see_public_and_created_events(self):


