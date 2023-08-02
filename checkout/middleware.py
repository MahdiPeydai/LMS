from django.conf import settings

from checkout.models import Cart

import jwt


class CartCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'cart' in request.COOKIES:
            token = request.COOKIES.get('cart')
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            cart_id = token['cart']
            print(cart_id)
            cart = Cart.objects.get(id=cart_id)

            if (not cart.user) and request.user:
                cart.user = request.user.id
                cart.save()
        else:
            if request.user.is_authenticated:
                user = request.user
                if Cart.objects.filter(user=user.id).exists():
                    cart = Cart.objects.filter(user=user).first()
                else:
                    cart = Cart(user=user)
                    cart.save()
            else:
                cart = Cart()
                cart.save()

        request.cart = cart
        token = jwt.encode({'cart': cart.id}, settings.SECRET_KEY, algorithm='HS256')
        response = self.get_response(request)
        response.set_cookie('cart', token, max_age=86400)

        return response
