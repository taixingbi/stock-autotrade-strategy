from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=255)

    strategy1 = "strategy1"
    strategy2 = "strategy2"
    strategy3 = "strategy3"

    choices = [
        (strategy1, "strategy1"),
        (strategy2, "strategy2"),
        (strategy3, "strategy3"),
    ]
    mode = models.CharField(
        max_length= 255,
        choices= choices,
        default= strategy1,
    )

    active = models.BooleanField(default=False)
    sell_share = models.IntegerField(default=0)
    buy_share = models.IntegerField(default=0)
    sell_stop_percentage = models.IntegerField(default=1)
    buy_stop_percentage = models.IntegerField(default=1)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'model_stock'
 

class Order_crud:
    # def __init__(self):
    #     print("Buy_crud")
    
    def read(self):
        # print("read")
        all_entries = Order.objects.all()
        names = all_entries.values_list('name', flat=True)
        active = all_entries.values_list('active', flat=True)
        mode = all_entries.values_list('mode', flat=True)
        buyStopPercentages = all_entries.values_list('buy_stop_percentage', flat=True)
        buyShares = all_entries.values_list('buy_share', flat=True)

        sellStopPercentages = all_entries.values_list('sell_stop_percentage', flat=True)
        sellShares = all_entries.values_list('sell_share', flat=True)

        allRecords = tuple(zip(names, sellShares, sellStopPercentages, buyShares, buyStopPercentages, active, mode))
        return allRecords

    def update(self, name):
        record = Order.objects.filter(name= name).values('active').first()
        active = record['active']
        active = not active
        Order.objects.filter(name= name).update(active = active)
