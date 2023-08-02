from django.core.cache import cache

from checkout.models import Cart


class CartCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if cache.has_key(f'cart_session_{request.session.session_key}'):
            cart = cache.get(f'cart_session_{request.session.session_key}')
        else:
            if request.user.is_authenticated:
                if Cart.objects.filter(user=request.user).exists():
                    cart = Cart.objects.filter(user=request.user).first()
                else:
                    cart = Cart(user=request.user)
                    cart.save()
            else:
                cart = Cart()
                cart.save()
        cache.set(f'cart_session_{request.session.session_key}', cart)
        response = self.get_response(request)
        return response
