from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator


"""This file contains the models for the main app of the Katisha project
The models are:
- Passenger, which is a profile for the user model from settings.AUTH_USER_MODEL
- Company, which is the company that owns the vehicles
- Vehicle, which is the vehicle that the company owns
- Route, which has the origin and destination of the route
- Ticket, which is the ticket that the passenger buys which has a route and vehicle relationship
, and price fields.
- Wallet, which is the wallet that the passenger has with a balance field
"""

# Create a new model named Wallet that inherits from models.Model
# Wallet has a balance field
# Wallet has the ability to top up the balance

class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def top_up(self, amount):
        self.balance += amount
        self.save()

    def __str__(self):
        return f"{self.balance} RWF"

# Create a new model named Passenger that inherits from models.Model
# Passenger has a one-to-one relationship with the User model from settings.AUTH_USER_MODEL
# Passenger is a profile and has phone and birthdate fields
# override the __str__ method to return the username of the user
class Passenger(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    birthdate = models.DateField()
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.wallet:
            self.wallet = Wallet.objects.create()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    

# create a vehicle model
# vehicle has a plate number, capacity, and company fields
# override the __str__ method to return the plate number and company name

# Create a new model named Company that inherits from models.Model
# Company has a name field
# Company has a one-to-many relationship with the Vehicle model
# override the __str__ method to return the name of the company
class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    plate_number = models.CharField(max_length=9, unique=True, validators=[RegexValidator(r'^RA[A-Z]\s\d{3}\s[a-z]$')])
    capacity = models.PositiveIntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plate_number} - {self.company.name}"
    

#create a route model that has an origin and destination fields
# override the __str__ method to return the origin and destination
class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origin} - {self.destination}"
    

# Create a new model named Ticket that inherits from models.Model
# Ticket has a passenger, route, vehicle, and price fields

class TicketTemplate(models.Model):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.route} - {self.vehicle} - {self.price} - {self.inventory}"

class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    ticket_template = models.ForeignKey(TicketTemplate, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger} - {self.ticket_template}"
    

