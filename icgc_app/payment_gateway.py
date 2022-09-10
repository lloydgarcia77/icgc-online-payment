from xendit import EWallet
import xendit  

from django.conf import settings


def create_payment(data): 
    xendit.api_key = settings.XENDIT_API_KEY_DEV_PRIVATE

    
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
            "success_redirect_url": "http://127.0.0.1:8000",
            "failure_redirect_url": "http://127.0.0.1:8000",
            "cancel_redirect_url": "http://127.0.0.1:8000",
        },
        basket=cart,
    ) 

    return ewallet_charge



