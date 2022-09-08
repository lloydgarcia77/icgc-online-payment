from django.shortcuts import render, get_object_or_404
from django.http import (
    JsonResponse,
    Http404,
    HttpResponseRedirect
) 
from django.utils.html import strip_tags 
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.db.models import Q, Sum, F, Avg
from django.db.utils import IntegrityError, DataError
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.core.files import File
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils.timezone import make_aware  

 
from icgc_app import (
    models,
    forms, 
    # custom_decorator,
)   
from django.conf import settings 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  


# NOTE: Error Pages

def error_404(request, exception):
    return render(request, "error/error_404.html", {})


def error_500(request):
    return render(request, "error/error_500.html", {})


def index(request, *args, **kwargs): 
    template_name = 'index.html'

    games = models.Game.objects.all().order_by('-date_created')

    context = {
        'user': request.user, 
        'games': games,
    }
    return render(request, template_name, context)

def about_us(request, *args, **kwargs): 
    template_name = 'about_us.html'
 
    context = {
        'user': request.user, 
    }
    return render(request, template_name, context)

def contact_us(request, *args, **kwargs): 
    template_name = 'contact_us.html'
 
    context = {
        'user': request.user, 
    }
    return render(request, template_name, context)


# NOTE: Login start's here


def game_items(request, *args, **kwargs): 
    template_name = 'game_item/game_item.html'
    name = kwargs.get('name') 
    game = get_object_or_404(models.Game, slug=name) 
    payment_methods = models.PaymentMethod.objects.all()
    data = dict()

    if request.is_ajax():
        if request.method == 'POST':
            
            print(request.POST)
            formData = {**request.POST}
            formData.pop('csrfmiddlewaretoken')
            email = formData.get('email',[''])[0]
            contact = formData.get('contact',[''])[0]
            pm_id = formData.get('pm_id',[''])[0]
            amt_id = formData.get('amt_id',[''])[0]
            pm = get_object_or_404(models.PaymentMethod, id=pm_id)
            amt = get_object_or_404(models.Amount, id=amt_id) 
            email_context = {
                'game': game,
                'email': email,
                'contact': contact,
                'pm': pm,
                'amt': amt,
            }

            print(email)

            # from_email = 'lloydgarcia77@gmail.com'
            from_email = 'icaregamecredits@gmail.com'
            to = 'lloydgarcia77@gmail.com'
            
            subject = 'ICareGameCredits Purchase Order Receipt'
            html_message = render_to_string('email/transaction_success.html', email_context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                from_email,
                [email,],
                html_message=html_message,
            ) 
            data['is_valid'] = True
        return JsonResponse(data)

    context = {
        'game': game,
        'payment_methods': payment_methods,
    }
    return render(request, template_name, context)


def game_get_amount_details(request, *args, **kwargs):
    data = dict()
    name = kwargs.get('name') 
    game = get_object_or_404(models.Game, slug=name) 
    id = kwargs.get('id')

    amt = get_object_or_404(models.Amount, id=id, game=game)
    if request.is_ajax():
        if request.method == 'POST':
            data['amt_id'] = amt.id
            data['amt'] = amt.amount
            data['pte'] = amt.points_to_earn
        return JsonResponse(data)
    else:
        raise Http404()


def game_get_payment_method_details(request, *args, **kwargs):
    data = dict()
    id = kwargs.get('id') 
    if request.is_ajax():
        
        if request.method == 'POST':
            pm = get_object_or_404(models.PaymentMethod, id=id)
            data['pm_id'] = pm.id
            data['pm'] = pm.name
        return JsonResponse(data)
    else: 
        raise Http404()

 

