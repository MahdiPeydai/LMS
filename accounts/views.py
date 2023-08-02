from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .forms import UserLoginForm, UserRegisterForm
from checkout.models import Cart, CartItems

import jwt


class Register(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')


class Login(View):
    def get(self, request):
        form = UserLoginForm()
        next_url = request.GET.get('next')
        return render(request, 'accounts/login.html', {'form': form, 'next_url': next_url})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_cart = Cart.objects.filter(user=user).first()
            if 'cart' in request.COOKIES:
                token = request.COOKIES.get('cart')
                token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                cookie_cart_id = token['cart']
                for item in CartItems.objects.filter(cart__id=cookie_cart_id).all():
                    item.cart = user_cart
                    item.save()
                Cart.objects.filter(id__exact=cookie_cart_id).delete()
            auth_login(request, user)
            next_url = request.POST['next_url']
            if next_url == "None":
                next_url = 'home'
            token = jwt.encode({'cart': user_cart.id}, settings.SECRET_KEY, algorithm='HS256')
            response = HttpResponseRedirect(next_url)
            response.set_cookie('cart', token, max_age=86400)
            return response
        else:
            messages.error(request, 'ایمیل یا رمز عبور صحیح نمی‌باشد')
            return redirect('login')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')
