from django.db import models

# Create your models here.

# This is basically a way to represent SQL tables, one class represents a table
# Django basically abstracts away the need to do actual SQL queries


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} - {self.code} Airport"


class Flight(models.Model):
    # Related name allows us to reference a Flight from an Airport
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival')
    duration = models.IntegerField()

    def __str__(self):
        return f"Flight No {self.id}: {self.origin} -> {self.destination}"

    def is_valid_flight(self):
        # Return the condition for the flight to be valid
        return self.origin != self.destination and self.duration < 0


class Passenger(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # Note that a passenger may be on multiple flights (not sure how but ok)
    # A Passenger is "related" to a Flight by the related_name known as 'passengers'
    flights = models.ManyToManyField(Flight, blank=True, related_name='passengers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


