from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json

from catalog.models import Offer
from cart.forms import CartAddProductForm
from nda_email.forms import ContactForm
from nda_email.email_sender import EmailSender
from nda_email.captcha import get_client_ip, yandex_captcha_validation


CART_SESSION_ID = 'cart'


def get_cart(request):
    # Создаем корзину для сессии
    cart = request.session.get(CART_SESSION_ID)
    if not cart:
        # Сохраняем пустую корзину в сессии
        cart = request.session[CART_SESSION_ID] = {}
    return cart


def save_cart(request):
    cart = get_cart(request)
    # Обновление сессии cart/0
    request.session[CART_SESSION_ID] = cart
    # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
    request.session.modified = True
    return cart


@require_POST
def cart_add(request, offer_id):
    cart = get_cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    item_add_form = CartAddProductForm(request.POST)
    
    if not item_add_form.is_valid():
        raise ValidationError('Invalid form')
        
    item_add_form_data = item_add_form.cleaned_data
    offer_id = str(offer.id)
    
    if offer_id not in cart:
        cart[offer_id] = {'quantity': item_add_form_data['quantity']}
    else:
        cart[offer_id]['quantity'] += item_add_form_data['quantity']
    
    save_cart(request)
    
    context = {
        'offers_in_cart': len(cart),
    }
    
    return render(request, 'cart/cart.html', context)


def cart_remove(request, offer_id):
    cart = get_cart(request)
    offer = get_object_or_404(Offer, id=offer_id)
    offer_id = str(offer.id)
    if offer_id in cart:
        del cart[offer_id]
    save_cart(request)
    return render(request, 'cart/cart_popup.html')


def cart_clear(request):
    if request.session.get(CART_SESSION_ID):
        del request.session[CART_SESSION_ID]
        request.session.modified = True


def get_cart_offers(request):
    cart = get_cart(request)
    offers = Offer.visible.filter(id__in=cart.keys())
    for offer in offers:
        offer_id = str(offer.id)
        offer_cart_record = cart.get(offer_id, None)
        if offer_cart_record is None:
            offer.quantity = 0
            print("offer_cart_record is None, which was not expected. Fallback to 0")
            continue
        offer.quantity = offer_cart_record.get('quantity', 0)
    return offers


def cart_modal(request):
    form = ContactForm()
    offers = get_cart_offers(request)
    return render(request, 'cart/cart_modal.html', {'offers': offers, 'form': form})


@require_POST
def cart_submit(request):
    form = ContactForm(request.POST)
    token = request.POST.get('smart-token')
    client_ip = get_client_ip(request)
    offers = get_cart_offers(request)
    if not yandex_captcha_validation(token, client_ip):
        response = render(request, 'nda_email/contactform.html', {'contact_form': form})
        response['HX-Trigger'] = json.dumps({"showError": "Докажите что вы не робот"})
        return response
    if form.is_valid():
        try:
            EmailSender.send_messages(request, offers)
        except Exception as e:
            print(f'email_send failed due to: {e}')
            response = HttpResponse(status=500)
            response['HX-Trigger'] = json.dumps({"showError": "Сообщение не отправлено"})
            return response
        cart_clear(request)
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "showMessage": "Запрос отправлен"
                })
            })
    return render(request, 'nda_email/contactform.html', {'contact_form': form})
