from checkout.models import Cart


class AnonymousCart:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (not request.user.is_authenticated) and ('cart' not in request.COOKIES):
            cart = Cart()
            cart.save()
            response.set_cookie('cart', cart.id)
        return response
