from django.views import View
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache

from .forms import UserLoginForm, UserRegisterForm
from checkout.models import Cart, CartItems


class Register(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                cache.delete(f'cart_session_{request.session.session_key}')
                auth_logout(request)
            user = form.save()
            auth_login(request, user)
            user_cart = Cart.objects.get(id=request.COOKIES.get('cart'))
            user_cart.user = user
            user_cart.save()
            cache.set(f'cart_session_{request.session.session_key}', user_cart)
            response = HttpResponseRedirect(reverse('dashboard'))
            response.set_cookie('cart', '', max_age=0)
            return response
        else:
            messages.error(request, 'دوباره سعی کنید')
            return redirect('register')


class Login(View):
    def get(self, request):
        form = UserLoginForm()
        next_url = request.GET.get('next')
        return render(request, 'accounts/login.html', {'form': form, 'next_url': next_url})

    def post(self, request):
        if request.user.is_authenticated:
            cache.delete(f'cart_session_{request.session.session_key}')
            auth_logout(request)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            next_url = request.POST['next_url']
            if next_url == "None":
                next_url = reverse('home')
            auth_login(request, user)
            user_cart = Cart.objects.filter(user=user).first()
            if user_cart:
                cache.set(f'cart_session_{request.session.session_key}', user_cart)
                if 'cart' in request.COOKIES:
                    for item in CartItems.objects.filter(cart__id=request.COOKIES.get('cart')).all():
                        if not CartItems.objects.filter(cart=user_cart, course=item.course).exists():
                            item.cart = user_cart
                            item.save()
                    Cart.objects.get(id=request.COOKIES.get('cart')).delete()
            else:
                if 'cart' in request.COOKIES:
                    user_cart = Cart.objects.get(id=request.COOKIES.get('cart'))
                    user_cart.user = user
                    user_cart.save()
                    for item in CartItems.objects.filter(cart__id=request.COOKIES.get('cart')).all():
                        item.cart = user_cart
                        item.save()
                else:
                    user_cart = Cart(user=request.user)
                    user_cart.save()
                cache.set(f'cart_session_{request.session.session_key}', user_cart)
            response = HttpResponseRedirect(next_url)
            response.set_cookie('cart', '', max_age=0)
            return response
        else:
            messages.error(request, 'ایمیل یا رمز عبور صحیح نمی‌باشد')
            return redirect('login')


@login_required
def logout(request):
    cache.delete(f'cart_session_{request.session.session_key}')
    auth_logout(request)
    return redirect('login')
