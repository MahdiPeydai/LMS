from django.views import View
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache

from .forms import UserLoginForm, UserRegisterForm
from django.contrib.contenttypes.models import ContentType
from checkout.models import Cart, CartItems
from accounts.models import Guest


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
                guest_cart = None
            else:
                guest_cart = cache.get(f'cart_session_{request.session.session_key}')
                cache.delete(f'cart_session_{request.session.session_key}')
                Guest.objects.filter(session_id=request.session.session_key).delete()
                request.session.flush()
            user = form.save()
            auth_login(request, user)
            if guest_cart:
                guest_cart.user_type = ContentType.objects.get_for_model(user)
                guest_cart.user_id = user.id
                cache.set(f'cart_session_{request.session.session_key}', guest_cart)
            return redirect('dashboard')
        else:
            messages.error(request, 'دوباره سعی کنید')
            return redirect('register')


class Login(View):
    def get(self, request):
        form = UserLoginForm()
        next_url = request.GET.get('next')
        return render(request, 'accounts/login.html', {'form': form, 'next_url': next_url})

    def post(self, request):
        next_url = request.POST['next_url']
        if next_url == "None":
            next_url = reverse('home')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            if request.user.is_authenticated:
                guest_cart = None
                cache.delete(f'cart_session_{request.session.session_key}')
                auth_logout(request)
            else:
                guest_cart = cache.get(f'cart_session_{request.session.session_key}')
                cache.delete(f'cart_session_{request.session.session_key}')
                Guest.objects.filter(session_id=request.session.session_key).delete()
                request.session.flush()
            auth_login(request, user)
            user_cart = Cart.objects.filter(user_type=ContentType.objects.get_for_model(user), user_id=user.id).first()
            if user_cart:
                if guest_cart:
                    for item in CartItems.objects.filter(cart=guest_cart).all():
                        if not CartItems.objects.filter(cart=user_cart, course=item.course).exists():
                            item.cart = user_cart
                            item.save()
                        else:
                            item.delete()
                    guest_cart.delete()
                cache.set(f'cart_session_{request.session.session_key}', user_cart)
            else:
                if guest_cart:
                    guest_cart.user_type = ContentType.objects.get_for_model(user)
                    guest_cart.user_id = user.id
                    guest_cart.save()
                    cache.set(f'cart_session_{request.session.session_key}', guest_cart)
            return redirect(next_url)
        else:
            messages.error(request, 'ایمیل یا رمز عبور صحیح نمی‌باشد')
            return redirect('login')


@login_required
def logout(request):
    cache.delete(f'cart_session_{request.session.session_key}')
    auth_logout(request)
    return redirect('login')
