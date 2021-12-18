
#### run aws ubuntu 18.04
https://www.digitalocean.com/community/tutorials/how-to-install-the-django-web-framework-on-ubuntu-18-04

```
python3 -m venv my_env
source my_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### packaging up your model changes
del all __pycache__ and mydatabase
```
python manage.py makemigrations model
python manage.py migrate
```

#### create supersuer
```
python manage.py createsuperuser
```

#### run local
```
python manage.py runserver 0.0.0.0:8083
```

#### aws 
```
ssh -i "hunter.pem" ubuntu@ec2-18-220-148-40.us-east-2.compute.amazonaws.com
http://18.220.148.40:8083/
```

### kill port
mac os
```
kill -9 $(lsof -ti:8083)
```
ubuntu
```
sudo kill -9 `sudo lsof -t -i:8083`
```

#### instrument_id
'UVXY': '158d12a1-9bb1-46e9-acde-888c5096b269'
'VXX':  'dc4e0c0e-cacd-4754-97a2-8c7958fd1ef8'
'TQQQ': '91f7ea28-e413-4ca4-b9fa-91f5822f8b8d'

### response 
res = stockSelltrailingStop(name, share, sell_stop_percentages)
```
{'detail': 'Not enough shares to sell.'}
```
```
{'detail': 'Not enough shares to sell.'}
```
```
404 Client Error: Not Found for url: https://api.robinhood.com/quotes/?symbols=UVXYA
```


res = stockBuytrailingStop(name, share, sell_stop_percentages)
```
'id': '61be0a5a-f518-4d6f-a5d4-2a0d7aaa791d', 'ref_id': '34a6c0ec-d950-4d7c-aa34-1d126d124df0', 'url': 'https://api.robinhood.com/orders/61be0a5a-f518-4d6f-a5d4-2a0d7aaa791d/', 'account': 'https://api.robinhood.com/accounts/633269444/', 'position': 'https://api.robinhood.com/positions/633269444/158d12a1-9bb1-46e9-acde-888c5096b269/', 'cancel': 'https://api.robinhood.com/orders/61be0a5a-f518-4d6f-a5d4-2a0d7aaa791d/cancel/', 'instrument': 'https://api.robinhood.com/instruments/158d12a1-9bb1-46e9-acde-888c5096b269/', 'instrument_id': '158d12a1-9bb1-46e9-acde-888c5096b269', 'cumulative_quantity': '0.00000000', 'average_price': None, 'fees': '0.00', 'state': 'unconfirmed', 'pending_cancel_open_agent': None, 'type': 'market', 'side': 'buy', 'time_in_force': 'gtc', 'trigger': 'stop', 'price': '17.04000000', 'stop_price': '16.23000000', 'quantity': '1.00000000', 'reject_reason': None, 'created_at': '2021-12-18T16:20:42.337962Z', 'updated_at': '2021-12-18T16:20:42.337981Z', 'last_transaction_at': '2021-12-18T16:20:42.337962Z', 'executions': [], 'extended_hours': False, 'override_dtbp_checks': False, 'override_day_trade_checks': False, 'response_category': None, 'trailing_peg': {'type': 'percentage', 'percentage': 1}, 'stop_triggered_at': None, 'last_trail_price': None, 'last_trail_price_updated_at': None, 'dollar_based_amount': None, 'total_notional': {'amount': '17.04', 'currency_code': 'USD', 'currency_id': '1072fc76-1862-41ab-82c2-485837590762'}, 'executed_notional': None, 'investment_schedule_id': None, 'is_ipo_access_order': False, 'ipo_access_cancellation_reason': None, 'ipo_access_lower_collared_price': None, 'ipo_access_upper_collared_price': None, 'ipo_access_upper_price': None, 'ipo_access_lower_price': None, 'is_ipo_access_price_finalized': False, 'is_visible_to_user': True, 'has_ipo_access_custom_price_limit': False}
```
```
{'detail': 'You can only purchase 47 shares of UVXY.'}
```


res = rs.orders.get_all_open_stock_orders()
```
{"id": "61bcff16-9af3-4351-8830-68366de047e3", "ref_id": "3031facc-1376-4008-ad11-1fc904f356cc", "url": "https://api.robinhood.com/orders/61bcff16-9af3-4351-8830-68366de047e3/", "account": "https://api.robinhood.com/accounts/633269444/", "position": "https://api.robinhood.com/positions/633269444/158d12a1-9bb1-46e9-acde-888c5096b269/", "cancel": "https://api.robinhood.com/orders/61bcff16-9af3-4351-8830-68366de047e3/cancel/", "instrument": "https://api.robinhood.com/instruments/158d12a1-9bb1-46e9-acde-888c5096b269/", "instrument_id": "158d12a1-9bb1-46e9-acde-888c5096b269", "cumulative_quantity": "0.00000000", "average_price": null, "fees": "0.00", "state": "unconfirmed", "pending_cancel_open_agent": null, "type": "market", "side": "buy", "time_in_force": "gtc", "trigger": "stop", "price": "17.00000000", "stop_price": "16.19000000", "quantity": "2.00000000", "reject_reason": null, "created_at": "2021-12-17T21:20:22.969690Z", "updated_at": "2021-12-17T21:20:22.969708Z", "last_transaction_at": "2021-12-17T21:20:22.969690Z", "executions": [], "extended_hours": false, "override_dtbp_checks": false, "override_day_trade_checks": false, "response_category": null, "trailing_peg": {"type": "percentage", "percentage": 1}, "stop_triggered_at": null, "last_trail_price": null, "last_trail_price_updated_at": null, "dollar_based_amount": null, "total_notional": {"amount": "34.00", "currency_code": "USD", "currency_id": "1072fc76-1862-41ab-82c2-485837590762"}, "executed_notional": null, "investment_schedule_id": null, "is_ipo_access_order": false, "ipo_access_cancellation_reason": null, "ipo_access_lower_collared_price": null, "ipo_access_upper_collared_price": null, "ipo_access_upper_price": null, "ipo_access_lower_price": null, "is_ipo_access_price_finalized": false, "is_visible_to_user": true, "has_ipo_access_custom_price_limit": false}
```

