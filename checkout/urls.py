from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_page, name='checkout'),
    path('course/<int:course_id>/enroll', views.course_enroll, name='course_enroll'),
    path('cart/', views.cart_page, name='cart'),
    path('cart/store', views.CartItemStore.as_view(), name='cart_item_store'),
    path('cart/destroy/<int:course_id>', views.CartItemDestroy.as_view(), name='cart_item_destroy'),
    path('payment/<int:payment_id>/information/post', views.payment_data_post, name='payment_data_post'),
    path('payment/transaction/<int:transaction_id>/result', views.transaction_result, name='transaction_result')
]
