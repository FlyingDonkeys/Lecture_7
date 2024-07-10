from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import *


# Create your views here.


def index(request):
    return render(request, 'flights/index.html', {
        "flights": Flight.objects.all()
    })


# Notice that the urlpattern has a variable flight_id in its path, we gotta use it here to get the data from the DB
# It is essential that URL pattern variables and view function parameters must match!
def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, 'flights/flight.html', {
        "flight": flight,
        # Use of related name here, Flight is related to Passenger by the related name "passengers"
        "passengers": flight.passengers.all(),
        # Exclude the passengers who are related to this flight and take all of such passengers
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if (request.method == "POST"):
        flight = Flight.objects.get(id=flight_id)
        passenger = Passenger.objects.get(id=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        # Note that reverse takes an argument the name of a particular view and renders it
        return HttpResponseRedirect(reverse("flight", args=[flight_id]))