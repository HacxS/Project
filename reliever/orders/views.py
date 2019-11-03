from django.shortcuts import render
from .models import OrderItem,Order
from .forms import OrderCreateForm,OrderCreate,HOSTEL_LIST
from cart.cart import Cart
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from paytm import Checksum
from django.http import HttpResponse


def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        print(request.POST)
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        get_lang = "/" + get_language() if get_language() else ''
        CALLBACK_URL = settings.HOST_URL  + settings.PAYTM_CALLBACK_URL
        order_id = Checksum.__id_generator__()
        bill_amount=0

        form = OrderCreate(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            mobno = form.cleaned_data['mobno']
            

            order = Order(username=request.user,name=name,address=address,email=email,mobno=mobno,order_id=order_id)
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            bill_amount = cart.get_total_price()
            cart.clear()

        if bill_amount:
            data_dict = {
                        'MID':MERCHANT_ID,
                        'ORDER_ID':order_id,
                        'TXN_AMOUNT': bill_amount,
                        'CUST_ID':email,
                        'MOBILE_NO': mobno,
                        'INDUSTRY_TYPE_ID':'Retail',
                        'WEBSITE': settings.PAYTM_WEBSITE,
                        'CHANNEL_ID':'WEB',
                        'CALLBACK_URL':CALLBACK_URL,#"http://127.0.0.1:8000/paytm/response"
                    }
            param_dict = data_dict
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
            print(param_dict)
            return render(request,"paytm/payment.html",{'paytmdict':param_dict})
        else:
            return HttpResponse("Bill Amount Could not find. ?bill_amount=10")
    else:
        form = OrderCreate()
    return render(request, 'orders/order/create.html', {'form': form,'username':request.user })