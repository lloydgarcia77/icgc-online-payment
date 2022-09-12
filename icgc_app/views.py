
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
    payment_gateway,
)   
from django.conf import settings 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  

# NOTE: Email Activation
from icgc_app.tokens import account_activation_token  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.html import strip_tags
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

import json

# NOTE: Error Pages

def error_404(request, exception):
    return render(request, "error/error_404.html", {})


def error_500(request):
    return render(request, "error/error_500.html", {})


# NOTE: Login

def login_page(request):
    template_name = "registration/login.html"  
    # NOTE: Redirects to the index page when trying to go back 
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("icgc_app:index"))
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
      
        user = authenticate(email=email, password=password) 
        if user:  
            if user.is_active and user.is_valid: 
                login(request, user) 
                # request.session.set_expiry(request.session.get_expiry_age())
                previous_page = request.GET.get('next', reverse("icgc_app:index"))
                return HttpResponseRedirect(previous_page)
            else:
                messages.error(request, "Your account is needs approval, Please contact your administrator!")
        else:
            messages.error(request, "Your account is INVALID!")
        
    return render(request, template_name)


def activation_page(request, uidb64, token):
    template_name = 'registration/acc_activation_complete.html'  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  

    status = False
    if user is not None and account_activation_token.check_token(user, token):
        # ! Identify if the user is an emb or else  
        user.is_active = True  
        user.is_valid = True  
        user.is_staff = True  
        user.save()  
        status = True

    context = {
        'status' : status
    }

    return render(request, template_name, context)


def registration_page(request):
    template_name = "registration/register.html"
    
    if request.method == 'GET':
        form = forms.RegistrationForm(request.GET or None)
    elif request.method == 'POST':
        form = forms.RegistrationForm(request.POST or None)  
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.is_staff = False
            instance.is_superuser = False
            instance.save()

            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email address'  
            message = render_to_string('registration/acc_active_email.html', {  
                # 'userRegForm': userRegForm,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(instance.pk)),  
                'token':account_activation_token.make_token(instance),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
 
            messages.success(request, "Registration successfuly \
                Please check your E-mail for activation link.")
            return HttpResponseRedirect(reverse("login"))

    context = {
        'form': form,
    }

    return render(request, template_name, context)

 

# NOTE: Index page

@csrf_exempt
def index(request, *args, **kwargs): 
    template_name = 'index.html'
    data = dict()

    games = models.Game.objects.all().order_by('-date_created')

    if request.is_ajax():
        if request.method == 'GET':
            games = models.Game.objects.all().order_by('-date_created')
        elif request.method == 'POST':
            search = request.POST.get('search')
            sort_order = request.POST.get('sort-order')
            if search.strip(): 
                order = "name" if int(sort_order) == 0 else "-name"
                games = models.Game.objects.all().filter(Q(name__icontains=search) | Q(title__icontains=search)).order_by(order)

        context = {
            'user': request.user, 
            'games': games,
        }

        data['html_table'] = render_to_string('game_item/game_list.html', context, request)
        

        return JsonResponse(data)
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

@login_required
def game_items(request, *args, **kwargs): 
    template_name = 'game_item/game_item.html'
    name = kwargs.get('name') 
    game = get_object_or_404(models.Game, slug=name) 
    payment_methods = models.PaymentMethod.objects.all()
    data = dict()

    if request.is_ajax():
        if request.method == 'POST':
             
            formData = {**request.POST}
            formData.pop('csrfmiddlewaretoken')
            email = formData.get('email',[''])[0]
            contact = formData.get('contact',[''])[0]
            pm_id = formData.get('pm_id',[''])[0]
            amt_id = formData.get('amt_id',[''])[0]
            pm = get_object_or_404(models.PaymentMethod, id=pm_id)
            amt = get_object_or_404(models.Amount, id=amt_id) 

            contact = '+63'+contact[1:]

            if email.strip():
                
                transaction = models.Transaction.objects.create(
                    user=request.user,
                    amount=amt,
                    payment_method=pm,
                    game=game, 
                    mobile_number=contact,
                )

                
                response = payment_gateway.create_payment(transaction)


                """
                    NOTE: https://www.programiz.com/python-programming/methods/built-in/vars
                    NOTE: The vars() method returns the __dict__ (dictionary mapping) attribute of the given object.
                """
                transaction.charge_id = vars(response).get('id')
                transaction.save()
            
                email_context = {
                    'game': game,
                    'email': email,
                    'contact': contact,
                    'pm': pm,
                    'amt': amt,
                    'transaction': transaction,
                }

    
                from_email = 'icaregamecredits@gmail.com'
                # to = 'lloydgarcia77@gmail.com'
                
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

@login_required
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

@login_required
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

@login_required
def profile_page(request, *args, **kwargs):
    template = "profile/profile.html"
    user = request.user

    if request.method == 'GET':
        form = forms.ProfileForm(request.GET or None, instance=user)
    elif request.method == 'POST':
        form = forms.ProfileForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been successfully updated!")
            return HttpResponseRedirect(reverse("icgc_app:index"))

    context = {
        'user': user,
        'form': form,
    }

    return render(request, template, context=context)

@login_required
def transactions(request, *args, **kwargs): 
    template_name = 'transactions/transactions.html'
 
    context = {
        'user': request.user, 
    }
    return render(request, template_name, context)


# ! success
# ! cancell
# ! failure


@csrf_exempt
def payment_status_callback(request, *args, **kwargs):
    data = dict()

    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
        return JsonResponse(data)
    

    return render(request, 'payment_check_status/payment_check_status.html')
    
