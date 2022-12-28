from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from pages.models import QuoteRequest, Mechanic
import requests


def substring_after(s, delim):
    return s.partition(delim)[2]


def get_quotes(quote_request_pk):
    quote = QuoteRequest.objects.get(pk=quote_request_pk)
    mechanics_qs = Mechanic.objects.filter(city=quote.seller_address_state)
    quotes = list()
    for mechanic in mechanics_qs:
        quotes.append((mechanic, mechanic.checking_plans.all()))
    return quotes


def validate_link(request):
    request_step_template = 'request_step.html'
    validatation_step_template = 'validation_step.html' 
    quote_step_template = 'quote_step.html'
    error_template = 'error.html'
    context = {}

    if request.GET.get('form_id') == 'validate':
        publication_link = request.GET.get('publication_link')
        publication_id = "MLU-620915974".replace('-', '') # TODO: get proper id from publication_link
        API_ENDPOINT =  "https://api.mercadolibre.com/items/"
        query_response = requests.get(f"{API_ENDPOINT}{publication_id}?include_attributes=all")
        if query_response.status_code == 200:
            response_json = query_response.json()
            publication_title = ''
            seller_address_city = ''
            seller_address_state = ''
            seller_address_country = ''

            if 'title' in response_json:
                publication_title = response_json.get('title')
            if 'seller_address' in response_json:
                if 'city' in response_json.get('seller_address'):
                    seller_address_city = response_json.get('seller_address').get('city').get('name')
                if 'state' in response_json.get('seller_address'):
                    seller_address_state = response_json.get('seller_address').get('state').get('name')
                if 'country' in response_json.get('seller_address'):
                    seller_address_country = response_json.get('seller_address').get('country').get('name')

            if 'attributes' in response_json:
                for attribute in response_json.get('attributes'):
                    attribute_id = attribute.get('id')
                    value_name = attribute.get('value_name')
                    if attribute_id == 'SINGLE_OWNER':
                        single_owner = value_name
                    if attribute_id == 'KILOMETERS':
                        kilometers = value_name
                    if attribute_id == 'BRAND':
                        brand =  value_name
                    if attribute_id == 'MODEL':
                        model = value_name
                    if attribute_id == 'ENGINE':
                        engine = value_name
                    if attribute_id == 'FUEL_TYPE':
                        fuel_type = value_name
                    if attribute_id == 'TRANSMISSION':
                        transmission = value_name
                    if attribute_id == 'TRACTION_CONTROL':
                        taction_control = value_name
                    if attribute_id == 'STEERING':
                        steering = value_name
                    if attribute_id == 'TRIM':
                        trim = value_name
                    if attribute_id == 'VEHICLE_YEAR':
                        vehicle_year = value_name
                    if attribute_id == 'CONTACT_SCHEDULE':
                        phone_number = value_name
            
            quote_request = QuoteRequest.objects.create(
                publication_id = publication_id,
                publication_title = publication_title,
                vehicle_brand = brand,
                vehicle_model = model,
                vehicle_kilometers = kilometers,
                seller_address_city = seller_address_city,
                seller_address_state = seller_address_state,
                seller_address_country = seller_address_country
            )

            context = {
                'quote_request_pk': quote_request.pk,
                'publication_id': publication_id,
                'publication_title': publication_title,
                'vehicle_brand': brand,
                'vehicle_model': model,
                'vehicle_kilometers': kilometers
            }

            return render(request, validatation_step_template, context) 
        else:
            #TODO: contemplate non 200 response
            pass
    elif request.GET.get('form_id') == 'cotizar':
        if 'quote_request_pk' in request.GET:
            checking_plans = get_quotes(quote_request_pk=request.GET.get('quote_request_pk'))
            context = {'checking_plans': checking_plans}
            return render(request, quote_step_template, context)
        else:
            # Quote not found
            return render(request, error_template)
        return render(request, quote_step_template, context)
    else:
        return render(request, request_step_template, context)

    