from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from mysite.core import views
from django.views.generic import TemplateView
from datetime import datetime

from stock.strategy import *

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    # path('sell/', views.sell_view, name='sell'),
    path('order/', views.order_view, name='order'),
    path('api/test', views.Api.test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#--------------cron job--------------------------
class Apscheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.job = None
        self.seconds = 10
        self.traderStock = TraderStock()

    def start_job(self):
        self.job = self.scheduler.add_job(self.traderStock.process, 'interval', seconds=self.seconds)
        try:
            self.scheduler.start()
        except:
            pass

class ScheduleJobTest:
    def __init__(self):
        print("ScheduleJobTest")

    def job(self):
        print("\n job",datetime.now())

Apscheduler().start_job()