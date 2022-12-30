from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from pages.models import QuoteRequest, Mechanic
from django.contrib.auth.models import Group
from pages.forms import MechanicForm
import requests
import re


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
        publication_id = re.search('MLU-[0-9]+', publication_link)
        if not publication_id:
            # TODO: propagate error message
            return render(request, request_step_template)
        API_ENDPOINT =  "https://api.mercadolibre.com/items/"
        publication_id = publication_id.group(0).replace('-', '')
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
        if 'cotizar' in request.GET and 'quote_request_pk' in request.GET:
            checking_plans = get_quotes(quote_request_pk=request.GET.get('quote_request_pk'))
            context = {'checking_plans': checking_plans}
            return render(request, quote_step_template, context)
        elif 'wrong_car' in request.GET:
            return render(request, request_step_template)
        else:
            # Quote not found
            return render(request, error_template)
    else:
        return render(request, request_step_template, context)


def register_mechanic(request):
    if request.method == 'POST':
        form = MechanicForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            mechanic_group = Group.objects.get(name='Mechanic')
            mechanic_group.user_set.add(new_user)
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect("/admin/pages/mechanic/add/")
    form = MechanicForm()
    return render (request=request, template_name="register_mechanic.html", context={"register_form":form})

    