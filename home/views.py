from django.shortcuts import render
from django.views.decorators.cache import cache_page

from utils.get_offer_courses import get_offer_courses


@cache_page(60)
def home(request):
    context = {
        'offer_courses': get_offer_courses()
    }
    return render(request, 'home/home.html', context)
