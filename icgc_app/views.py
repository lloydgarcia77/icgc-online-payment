from django.shortcuts import render, get_object_or_404
from django.http import (
    JsonResponse,
    Http404,
    HttpResponseRedirect
) 
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




def game_items(request, *args, **kwargs): 
    template_name = 'game_item/game_item.html'
    name = kwargs.get('name')

    game = get_object_or_404(models.Game, slug=name) 

    context = {
        'game': game,
    }
    return render(request, template_name, context)