from django.core.cache import cache

from checkout.models import Cart


def get_cart(request):
    if request.user.is_authenticated:
        cart = cache.get(f'cart_session_{request.session.session_key}')
    else:
        cart = Cart.objects.get(id=request.COOKIES.get('cart'))
    return cart
