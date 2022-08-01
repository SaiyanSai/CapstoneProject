from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30,null=False,default='generic carmake')
    description = models.CharField(max_length=200,null=False,default='This is a carmake')
    def ___str___(self):
        return (self.name + "," + self.description)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerid = models.IntegerField(default=0)
    name = models.CharField(max_length=30,null=False,default="generic car")
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    type_choices = [
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon')
    ]
    type = models.CharField(null=False, max_length=20, choices=type_choices, default=SEDAN)
    def ___str___(self):
        return (self.name + "," + self.dealerid + "," + self.carmake + "," + self.type)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
