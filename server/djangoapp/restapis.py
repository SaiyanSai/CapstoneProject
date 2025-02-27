from pyexpat import features
#from urllib import request
import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, CategoriesOptions, EntitiesOptions, KeywordsOptions
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

import http.client


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url,*api_key,**kwargs):
    print(kwargs)
    y = json.dumps(kwargs)
    print (y)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if(api_key):
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
             response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(response.text)
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("POST to {}".format(url))
    print(json_payload)
    print(kwargs)
    try:
        response=requests.post(url, params=kwargs, json = json_payload)
    except:
        print("Eror occured at POST")
    if(response): 
        print(response.text)        

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["entries"]
        # For each dealer object
        for areview in reviews:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(car_year = areview.get("car_year"),purchase_date= areview.get("purdate"),dealership = areview["dealership"], name= areview["name"], purchase = areview["purchase"],
                                     review = areview["review"], id = areview["id"], car_make=areview["car_make"], car_model= areview["car_model"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
           # re_obj= DealerReview(dealership = areview["dealership"])
            results.append(review_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    kwargs = dict()
    api_key = "KFsl_uR0v8b1XMdcjBXAf3PHsajouzly9-EUiS1qY0Sp"
    url ="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/661252c6-375c-4783-bf6a-8f4e76fc3833"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    try:
        response = natural_language_understanding.analyze(text=text,features=Features(keywords=KeywordsOptions(sentiment=True,limit=1))).get_result()   
    except:
        response = "something went wrong"
        print("api error occured")
        return "neutral"
   # kwargs["text"] = text
   # kwargs["version"] = "2019-07-12"
   # json_result = get_request(url, api_key, kwargs)
    print(" One iterations/n")
    print(json.dumps(response))
    print(response["keywords"][0]["sentiment"]["label"])
    return response["keywords"][0]["sentiment"]["label"]
    

