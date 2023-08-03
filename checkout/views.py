from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .models import Cart, CartItems, Order, OrderItems, Payment, Transaction
from course.models import Course, UserEnrollment
from django.db.models import Count

import json
import requests

from utils.get_offer_courses import get_offer_courses
from utils.get_cart import get_cart


class CartItemStore(View):
    def post(self, request):
        cart = get_cart(request)
        data = json.load(request)
        course_id = data['course_id']
        course = Course.objects.get(id=course_id)
        new_item = CartItems(cart=cart, course=course)
        new_item.save()

        return JsonResponse({})


class CartItemDestroy(View):
    def delete(self, request, course_id):
        cart = get_cart(request)
        course = Course.objects.get(id=course_id)
        CartItems.objects.filter(cart=cart, course=course).delete()

        return JsonResponse({'cart_items': CartItems.objects.filter(cart=cart).count(),
                             'course_id': course_id})


def cart_page(request):
    cart = get_cart(request)
    if not CartItems.objects.filter(cart=cart).exists():
        cart_status = 'empty'
        context = {
            'offer_courses': get_offer_courses(),
            'status': cart_status
        }
    else:
        cart_status = 'full'
        courses = Course.objects.filter(cartitems__cart=cart).all()
        context = {
            'cart': cart,
            'status': cart_status,
            'courses': courses,
            'cart_total_price': 0,
        }
        for course in courses:
            context['cart_total_price'] += course.price

    return render(request, 'checkout/cart.html', context)


@login_required
def checkout_page(request):
    cart = get_cart(request)
    user = request.user
    new_order = Order(user=user)
    new_order.save()
    total = 0
    for course in CartItems.objects.filter(cart=cart).all():
        new_course = OrderItems(order=new_order, course=course.course, price=course.course.price)
        new_course.save()
        total += new_course.price
        course.delete()
    cart.delete()
    new_cart = Cart(user=user)
    cache.set(f'cart_session_{request.session.session_key}', new_cart)

    order_payment = Payment(order=new_order, total_amount=total)
    order_payment.save()

    context = {
        'courses': OrderItems.objects.filter(order=new_order).all(),
        'payment': order_payment,
        'total': total
    }

    return render(request, 'checkout/checkout.html', context)


@login_required
def course_enroll(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    new_order = Order(user=user)
    new_order.save()
    new_course = OrderItems(order=new_order, course=course, price=course.price)
    new_course.save()
    total = course.price
    order_payment = Payment(order=new_order, total_amount=total)
    order_payment.save()

    context = {
        'courses': [course],
        'payment': order_payment,
        'total': total
    }
    return render(request, 'checkout/checkout.html', context)


@login_required
def payment_data_post(request, payment_id):
    payment = Payment.objects.get(id=payment_id)

    new_transaction = Transaction(
        payment_id=payment_id,
    )
    new_transaction.save()

    callback_url = reverse('transaction_result', kwargs={'transaction_id': new_transaction.id})

    url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "merchant_id": "349F54A1-2DCF-4E2F-9A2D-98558951968A",
        "amount": payment.total_amount,
        "description": "بهنام کافه",
        "callback_url": request.build_absolute_uri(callback_url),
        "metadata": {
            'mobile': payment.order.user.phone,
            'email': payment.order.user.email
        }
    }
    while True:
        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            data = response_json['data']
            authority = data['authority']
            break

    new_transaction.authority = authority
    new_transaction.save()

    return redirect(f'https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}')


@login_required
def transaction_result(request, transaction_id):
    transaction_status = request.Status

    transaction = Transaction.objects.get(id=transaction_id)
    if transaction_status == 'OK':
        url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "merchant_id": "349F54A1-2DCF-4E2F-9A2D-98558951968A",
            "amount": transaction.payment.total_amount,
            "authority": transaction.authority
        }
        while True:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response_json = response.json()
                data = response_json['data']
                if data['code'] == 100 or data['code'] == 101:
                    transaction.status = 'successful'
                    transaction.details = 'پرداخت با موفقیت انجام شد'
                    transaction.save()
                else:
                    transaction.status = 'fail'
                    transaction.details = 'مشکلی در عملیات پرداخت بوجود آمده، مبلغ کسر شده بعد از ۴۸ساعت به حساب شما ' \
                                          'باز میگردد '
                    transaction.save()
                break
    else:
        transaction.status = 'fail'
        transaction.details = 'عملیات پرداخت لغو شد'
        transaction.save()

    offer_courses = Course.objects.annotate(num_enrollments=Count('enrollments')).order_by('num_enrollments')[:4]
    context = {
        'transaction': transaction,
        'offer_courses': []
    }
    for course in offer_courses:
        context['offer_courses'].append({
            'course': course,
            'categories': course.categories.all(),
            'course_enrolled_users': UserEnrollment.objects.filter(course=course).count(),
        })

    return render('checkout/payment/payment.html', context)
