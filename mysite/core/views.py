from django.views.generic import TemplateView
from django.http import JsonResponse
from model.log import Log_crud
from model.order import Order_crud

from stock.module import *
from django.template.response import TemplateResponse

log_crud = Log_crud()
order_crud = Order_crud()
# views
class Home(TemplateView):
    template_name = 'home.html'

def order_view(request, template_name="order.html"):
    if request.POST:
        name_active = request.POST['active']
        order_crud.update(name_active)

    args = {}
    logs = log_crud.read()
    orders = order_crud.read()
    stocks= []
    for order in orders:
        stocks.append( order +  (str(CheckPrice(order[0]).live()), ) )
    args['stocks'] = stocks
    args['logs'] = logs[:10]
    return TemplateResponse(request, template_name, args)

class Api(): 
    def test(request):  
        print("\n\n*************************************test*************************************")
        
        # log_crud = Log_crud()
        # # log_crud.create( str(datetime.now()), "this is log test")
        # # logs = log_crud.read()
        # # print(logs)
        # log_crud.delete()

        dataJson= {
            "test": "test"
        }

        return JsonResponse(dataJson)
