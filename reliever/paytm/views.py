from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

from . import Checksum


from paytm.models import PaytmHistory
from orders.models import Order

from django.core.mail import send_mail

'''def payment(request):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = settings.HOST_URL  + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()

    bill_amount = 1000
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': bill_amount,
                    'CUST_ID':'albertgovind17@gmail.com',
                    'MOBILE_NO': '7777777789',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':CALLBACK_URL,#"http://127.0.0.1:8000/paytm/response"
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        print(param_dict)
        return render(request,"paytm/payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")
'''

@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        user=request.POST['ORDERID']
        RES = int(request.POST['RESPCODE'])
        for key in request.POST:
            data_dict[key] = request.POST[key]

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            PaytmHistory.objects.create(user=user, **data_dict)
            if RES == 1:
                curr_user = Order.objects.filter(order_id=user)[0]
                curr_user.paid=True
                username = curr_user.username
                mail_body = 'payment confirm with order id %s and tranction id %s of %s INR'%(user,data_dict['TXNID'],data_dict['TXNAMOUNT'])
                send_mail(
                    'Payment Confirmation from Campussquare',
                    mail_body,
                    'albertgovind17@gmail.com',
                    [curr_user.email],
                    fail_silently=False,
                )
                curr_user.save()
            return render(request,"paytm/response.html",{"paytm":data_dict,"username": username})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)