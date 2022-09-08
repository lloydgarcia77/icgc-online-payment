from django.urls import path
from icgc_app import views
from django.views.generic import TemplateView

app_name = "icgc_app"

urlpatterns = [
    path('', views.index, name='index'), 
    path('game-item/<slug:name>/', views.game_items, name='game_items'), 
    path('game-item/<slug:name>/<uuid:id>/', views.game_get_amount_details, name='game_get_amount_details'),  
    path('game-item/<slug:name>/payment-method/<uuid:id>/', views.game_get_payment_method_details, name='game_get_payment_method_details'), 
    path('about-us/', views.about_us, name='about_us'), 
    path('contact-us/', views.contact_us, name='contact_us'), 
]