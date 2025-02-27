from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def aboutus(request):
    return render(request, 'djangoapp/aboutus.html')
# ...


# Create a `contact` view to return a static contact page
def contactus(request):
    return render(request, 'djangoapp/contactus.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)
# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html")
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['psw']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "https://e8cae35e.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    kw ={}
    context={}
    url = "https://e8cae35e.us-south.apigw.appdomain.cloud/api/review"
    kw["dl"]=dealer_id
    ky = json.dumps(kw)   #i know im juggling a lot of dictionaries 
    ks = json.loads(ky)   # i used those to test my code and i am too afraid to delete them now 
    reviews = get_dealer_reviews_from_cf(url, **ks)
    context["reviews"] = reviews
    context["dealer_id"] = dealer_id
    #review_list = ' //t'.join([areview.sentiment for areview in reviews])
    return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    context={}
    ks={}
    ks["id"] = dealer_id
    cars = []
    url = "https://e8cae35e.us-south.apigw.appdomain.cloud/api/dealership"
    dealer = get_dealers_from_cf(url, **ks)
    cars = CarModel.objects.filter(dealerid = dealer_id)
    print(cars)
    user = request.user
    print (user)
    context["cars"] = cars
    context["dealer"] = dealer[0]
    context["dealer_id"] = dealer_id

    if(request.method == "GET"):
        return render(request, 'djangoapp/add_review.html', context)
    if (request.method == "POST"):    
        review = dict()
        json_payload = dict()
        url = "https://e8cae35e.us-south.apigw.appdomain.cloud/api/review"
        if(request.user.is_authenticated):
            review["id"] =request.POST['car']
            car = get_object_or_404(CarModel, pk=review["id"])
            review["name"] = user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            if 'purchasecheck' in request.POST:
                review["purchase"] = True
            else:
                review["purchase"] = False
            review["another"] = "another Field"
            review["purchase_date"] = request.POST['dateofpurchase']
            print(car.carmake.name)
            print(car.name)
            print(car.dateofmake.year)
            review["car_make"] = car.carmake.name
            review["car_model"] = car.name
            review["car_year"] = car.dateofmake.year
            json_payload["review"] = review
            post_request(url, json_payload)
            return HttpResponseRedirect(reverse('djangoapp:index'))
        else:
            return HttpResponse("Not Authenticated")

