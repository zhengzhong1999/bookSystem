from django.db import models
from django.contrib.auth.models import Permission, User


class Flight(models.Model):
    user = models.ManyToManyField(User, default=1)
    name = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100, null=True)
    arrive_city = models.CharField(max_length=100, null=True)
    departure_airport = models.CharField(max_length=100, null=True)
    arrive_airport = models.CharField(max_length=100, null=True)
    departure_time = models.DateTimeField(null=True)
    arrive_time = models.DateTimeField(null=True)
    capacity = models.IntegerField(default=0, null=True)
    price = models.FloatField(default=0, null=True)
    book_sum = models.IntegerField(default=0, null=True)
    first_price = models.FloatField(default=0, null=True)
    first_capacity = models.IntegerField(default=0, null=True)
    first_book_sum = models.IntegerField(default=0, null=True)
    distance = models.FloatField(default=0,null=True)

class Flight_order(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=30,null=True)
    name = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100, null=True)
    arrive_city = models.CharField(max_length=100, null=True)
    departure_airport = models.CharField(max_length=100, null=True)
    arrive_airport = models.CharField(max_length=100, null=True)
    departure_time = models.DateTimeField(null=True)
    arrive_time = models.DateTimeField(null=True)
    capacity = models.IntegerField(default=0, null=True)
    price = models.FloatField(default=0, null=True)
    book_sum = models.IntegerField(default=0, null=True)
    distance = models.FloatField(default=0, null=True)
    payment = models.IntegerField(default=0,null=True)

class Customer(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=30)
    distance = models.FloatField(default=0)


    def __str__(self):
        return self.name


class Payment(models.Model):
    email = models.CharField(max_length=30)
    bank_account = models.IntegerField(default=0)

    def __str__(self):
        return self.email


