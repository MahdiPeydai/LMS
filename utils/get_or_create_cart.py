from django.core.cache import cache

from checkout.models import Cart


def get_cart(request):
    user = request.user
    if user.is_authenticated:
        user_cart = Cart.objects.filter(user=user).first()
        if not user_cart:
            user_cart = Cart.objects.create(user_type='authenticated', user_id=user.id)
        cache.set(f'cart_session_{request.session.session_key}', user_cart)
    else:

    cart = cache.get(f'cart_session_{request.session.session_key}')
    return cart
