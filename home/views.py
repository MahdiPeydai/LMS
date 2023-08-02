from django.shortcuts import render

from utils.get_offer_courses import get_offer_courses


def home(request):
    context = {
        'offer_courses': get_offer_courses()
    }
    return render(request, 'home/home.html', context)
