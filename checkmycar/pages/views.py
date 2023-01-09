from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from pages.models import QuoteRequest, Mechanic, CheckingPlan
from django.contrib.auth.models import Group
from pages.forms import MechanicForm, NewClientForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
import requests
import re
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm 


def substring_after(s, delim):
    return s.partition(delim)[2]


def get_quotes(quote_request_pk):
    quote = QuoteRequest.objects.get(pk=quote_request_pk)
    mechanics_qs = Mechanic.objects.filter(city=quote.seller_address_state)
    quotes = list()
    for mechanic in mechanics_qs:
        quotes.append((mechanic, mechanic.checking_plans.all()))
    return quotes


def parse_publication_response(query_response):
    response_json = query_response.json()
    publication_title = ''
    seller_address_city = ''
    seller_address_state = ''
    seller_address_country = ''
    phone_number = None


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

    return publication_title, brand, model, kilometers, seller_address_city, seller_address_state, \
          seller_address_country, phone_number
    

def validate_link(request):
    request_step_template = 'request_step.html'
    validatation_step_template = 'validation_step.html' 
    quote_step_template = 'quote_step.html'
    payment_template = 'payment_template.html'
    payment_confirmed_template = 'payment_confirmed.html'
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
            publication_title, brand, model, kilometers, seller_address_city, \
            seller_address_state, seller_address_country, phone_number = parse_publication_response(query_response)
            
            quote_request = QuoteRequest.objects.create(
                publication_id = publication_id,
                publication_title = publication_title,
                vehicle_brand = brand,
                vehicle_model = model,
                vehicle_kilometers = kilometers,
                seller_address_city = seller_address_city,
                seller_address_state = seller_address_state,
                seller_address_country = seller_address_country,
                phone_number = phone_number
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
            quote_request_pk = request.GET.get('quote_request_pk')
            context = {'checking_plans': checking_plans, 'quote_request_pk': quote_request_pk}
            return render(request, quote_step_template, context)
        elif 'wrong_car' in request.GET:
            return render(request, request_step_template)
        else:
            # Quote not found
            return render(request, error_template)
    elif 'plan_selected' in request.GET:
        # TODO: Payment logic
        plan_pk_selected = request.GET.get('plan_selected')
        quote_request_pk =  request.GET.get('quote_request_pk')
        checking_plan = CheckingPlan.objects.get(pk=plan_pk_selected)
        context = {'checking_plan': checking_plan, 'quote_request_pk': quote_request_pk}
        return render(request, payment_template, context)
    elif 'checking_plan_paid' in request.GET:    
        quote_request = QuoteRequest.objects.get(pk=request.GET.get('quote_request_pk'))
        checking_plan = CheckingPlan.objects.get(pk=request.GET.get('checking_plan_paid'))

        paid = True
        subject_client = 'Pago exitoso'
        message_client = 'La cotizacion fue pagada con exito. El mecanico se pondra en contacto con el vendedor del vehiculo'  
        client_email =  'joaquinpunales@gmail.com' 
        client_msg_html = render_to_string('emails/client_new_request_paid.html', {'quote_request': quote_request, 'checking_plan': checking_plan})

        send_mail(
            subject=subject_client,
            message=message_client,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client_email],
            html_message=client_msg_html,
        )

        subject_mechanic = 'Nueva cotizacion requerido'
        message_mechanic = 'Una cotizacion ha sido requerida'
        mechanic_email = 'joaquinpunales@gmail.com' 
        mechanic_msg_html = render_to_string('emails/mechanic_new_request_email.html', {'quote_request': quote_request, 'checking_plan': checking_plan})

        send_mail(
            subject=subject_mechanic,
            message=message_mechanic,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mechanic_email],
            html_message=mechanic_msg_html,
        )
        context = {'paid': paid}

        return render(request, payment_confirmed_template, context)
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
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return HttpResponseRedirect("/admin/pages/mechanic/add/")
    form = MechanicForm()
    return render (request, template_name="register_mechanic.html", context={"register_form":form})


def mechanic_portal(request, request_pk):
    generate_inform_template = 'generate_inform.html'
    mechanic_portal_template = "mechanic_portal.html"

    if 'inform_quote_request_pk' in request.GET:
        quote_request = QuoteRequest.objects.get(pk=request.GET.get('inform_quote_request_pk'))
        return render(request, template_name=generate_inform_template, context={'quote_request': quote_request})

    quote_requests = QuoteRequest.objects.all() #filter(pk=request_pk)
    return render(request, template_name=mechanic_portal_template, context={'quote_requests': quote_requests})


def client_requests(request):
    client_requests_template='client_requests.html'
    return render(request, template_name=client_requests_template, context={})


def client_login(request):
    import pdb;pdb.set_trace()
    client_login_template = 'clients_portal/client_login.html'
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, template_name=client_login_template, context={"login_form":form})


def client_signup(request):
    import pdb;pdb.set_trace()
    client_signup_template='clients_portal/client_signup.html'
    if request.method == "POST":
        form = NewClientForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewClientForm()
    return render (request=request, template_name=client_signup_template, context={"register_form":form})