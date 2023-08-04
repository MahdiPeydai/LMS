from django.core.cache import cache

from django.contrib.contenttypes.models import ContentType
from checkout.models import Cart
from accounts.models import Guest


def get_or_create_cart(request):
    cart = cache.get(f'cart_session_{request.session.session_key}')
    if not cart:
        user = request.user
        if user.is_authenticated:
            cart = Cart.objects.filter(user_type=ContentType.objects.get_for_model(user), user_id=user.id).first()
            if not cart:
                cart = Cart.objects.create(user_type=ContentType.objects.get_for_model(user), user_id=user.id)
        else:
            guest = Guest.objects.create(session_id=request.session.session_key)
            cart = Cart.objects.create(user_type=ContentType.objects.get_for_model(guest), user_id=guest.id)
        cache.set(f'cart_session_{request.session.session_key}', cart)
    return cart
