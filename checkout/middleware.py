from checkout.models import Cart


class GuestSession:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.session.session_key:
            request.session.create()
        return response
