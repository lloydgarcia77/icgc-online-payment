from xendit import EWallet
import xendit  
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import requests


xendit.api_key = settings.XENDIT_API_KEY_DEV_PRIVATE

 

def create_payment(data, request):  
    
    protocol = f'{request.scheme}://' 
    domain = get_current_site(request).domain  

   
    cart = []
    game_item = EWallet.helper_create_basket_item(
        reference_id = str(data.transaction_id),
        name = data.game.name,
        category = "Game",
        currency = "PHP",
        price = data.amount.amount,
        quantity = 1,
        type = "e-points",
        sub_category = "credit",
        metadata = {
            "reference_id":  str(data.reference_id),
            "buyer": data.user.get_full_name(),
        }
    )
    cart.append(game_item)

    ewallet_charge = EWallet.create_ewallet_charge(
        reference_id=str(data.reference_id),
        currency="PHP",
        amount=data.amount.amount,
        checkout_method="ONE_TIME_PAYMENT",
        # channel_code="PH_PAYMAYA",
        channel_code=data.payment_method.channel_code.upper(),
        channel_properties={
            "success_redirect_url": protocol + domain + str(reverse('icgc_app:success_page')),
            "failure_redirect_url": protocol + domain + str(reverse('icgc_app:failure_page')),
            "cancel_redirect_url": protocol + domain + str(reverse('icgc_app:cancel_page')),
        },
        # ! ERror
        # channel_properties={
        #     "success_redirect_url": 'https://developers.xendit.co/api-reference/#authentication',
        #     "failure_redirect_url": 'https://developers.xendit.co/api-reference/#authentication',
        #     "cancel_redirect_url": 'https://developers.xendit.co/api-reference/#authentication',
        # },
        basket=cart,
    ) 

    return ewallet_charge

def check_transaction_status(charge_id): 
    ewallet_charge = EWallet.get_ewallet_charge_status(
        charge_id=charge_id,
    )

    return ewallet_charge

def void_transaction(charge_id):
    response = requests.post(f"https://api.xendit.co/ewallets/charges/{charge_id}/void", auth=(settings.XENDIT_API_KEY_DEV_PRIVATE, ''))
    return response

def refund_transaction(charge_id):
    response = requests.post(f"https://api.xendit.co/ewallets/charges/{charge_id}/refunds", auth=(settings.XENDIT_API_KEY_DEV_PRIVATE, ''))
    return response

def list_refund_transaction(charge_id):
    response = requests.get(f"https://api.xendit.co/ewallets/charges/{charge_id}/refunds", auth=(settings.XENDIT_API_KEY_DEV_PRIVATE, ''))
    return response