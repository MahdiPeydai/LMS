from django.contrib import admin
from .models import Order, OrderItems, Payment, Transaction


admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Payment)
admin.site.register(Transaction)
