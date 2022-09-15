from django.urls import path
from icgc_app import views
from django.views.generic import TemplateView

app_name = "icgc_app"

urlpatterns = [
    path('', views.index, name='index'), 
    path('profile/', views.profile_page, name='profile_page'), 
    path('transactions/', views.transactions, name='transactions'), 
    path('transactions-status/<uuid:id>/', views.transaction_status, name='transaction_status'), 
    path('transactions-delete/<uuid:id>/', views.delete_transaction, name='delete_transaction'), 
    path('transactions-void/<uuid:id>/', views.void_transaction, name='void_transaction'), 
    path('transactions-refund/<uuid:id>/', views.refund_transaction, name='refund_transaction'), 
    path('transactions-list-refund/<uuid:id>/', views.list_refund_transaction, name='list_refund_transaction'), 
    path('game-item/<slug:name>/', views.game_items, name='game_items'), 
    path('game-item/<slug:name>/<uuid:id>/', views.game_get_amount_details, name='game_get_amount_details'),  
    path('game-item/<slug:name>/payment-method/<uuid:id>/', views.game_get_payment_method_details, name='game_get_payment_method_details'), 
    path('about-us/', views.about_us, name='about_us'), 
    path('contact-us/', views.contact_us, name='contact_us'), 
    path('payment_status_callback/', views.payment_status_callback, name='payment_status_callback'), 
    path('success-page/', views.success_page, name='success_page'), 
    path('failure-page/', views.failure_page, name='failure_page'), 
    path('cancel-page/', views.cancel_page, name='cancel_page'), 



    
]