from django.contrib import admin

from model.log import Log
from model.order import Order

@admin.register(Log, Order)
class  StockSellAdmin(admin.ModelAdmin):
    pass