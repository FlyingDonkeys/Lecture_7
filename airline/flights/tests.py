from django.db.models import Max
from django.test import Client, TestCase

from .models import Airport, Flight, Passenger

# Create your tests here.
class FlightTestCase(TestCase):

    # Set up stuff to add test data into sample database
    def setUp(self):

        # Create airports
        a1 = Airport.objects.create(code='aaa', city='City A')
        a2 = Airport.objects.create(code='bbb', city='City B')

        # Create flights
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)


    # Test some cases
    def test_departure_counts(self):
        a = Airport.objects.get(code='aaa')
        self.assertEqual(a.departure.count(), 3)

    def test_arrival_counts(self):
        a = Airport.objects.get(code='aaa')
        self.assertEqual(a.arrival.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code='aaa')
        a2 = Airport.objects.get(code='bbb')
        f1 = Flight.objects.create(origin=a1, destination=a2, duration=100)
        self.assertTrue(f1.is_valid_flight())

    def test_invalid_flight(self):
        a1 = Airport.objects.get(code='aaa')
        f1 = Flight.objects.create(origin=a1, destination=a1, duration=-100)
        self.assertFalse(f1.is_valid_flight())

    # Test whether page appears correctly
    def test_index(self):
        c = Client()
        response = c.get('/flights/')
        # Ensure that the url link can be accessed
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flights/index.html')
        self.assertEqual(response.context['flights'].count(), 3) # This counts the number of flights objects (we have 3 flights)

    # Test if a flight page for a valid flight appears correctly
    def test_valid_flight_page(self):
        c = Client()
        airport = Airport.objects.get(code='aaa')
        flight = Flight.objects.get(origin=airport, destination=airport)

        response = c.get(f'/flights/{flight.id}')

        # Assert that this url link works
        self.assertEqual(response.status_code, 200)

    # Test if a flight page for an invalid page doesnt appear
    def test_invalid_flight_page(self):
        c = Client()
        response = c.get(f'/flights/{-1}')

        # Assert that the url link doesnt work (negative id doesnt exist)
        self.assertEqual(response.status_code, 404)


    # Test adding passenger into a flight
    def test_flight_page_passengers(self):
        c = Client()
        flight_1 = Flight.objects.get(pk=1)
        # Creating data in the database in the test
        passenger_1 = Passenger.objects.create(first_name='John', last_name='Doe')
        passenger_2 = Passenger.objects.create(first_name='Mary', last_name='Poppins')

        # Note that a Passenger is related to its Flights with a related name "passengers"
        flight_1.passengers.add(passenger_1)
        flight_1.passengers.add(passenger_2)

        # Get flight with pk = 1
        response = c.get(f'/flights/{1}')
        # Check if adding 2 passengers into the flight really gives a
        # passenger count of 2 in the context passed into the web
        self.assertEqual(response.context['passengers'].count(), 2)


