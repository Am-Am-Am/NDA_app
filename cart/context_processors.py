from cart.views import get_cart_offers
from nda_email.forms import ContactForm


def cart(request):

    offers_in_cart = get_cart_offers(request)
    contact_form = ContactForm()
    return {'offers_in_cart': offers_in_cart, 'contact_form': contact_form}
