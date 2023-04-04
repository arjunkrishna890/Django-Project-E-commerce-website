from django.shortcuts import render,redirect
from accounts.models import Products
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from .models import  CustomerCart
from .models import Cardorder
from django.conf import settings
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

# Create your views here.


def home(request):
    products  = Products.objects.filter(is_active='1')
    if request.user.is_authenticated:
        count = len(CustomerCart.objects.filter(customer = request.user))
        customercarts = CustomerCart.objects.filter(customer = request.user)
        return render(request,'userlog.html',{'products':products,'count':count,'customercarts': customercarts})
    return render(request,'userlog.html',{'products':products})

def logincustomer(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff == 1:
                return redirect('/')
            else:
                auth.login(request, user)
                return redirect('/customer')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/customer/login')

    else:
        return render(request,'logincustomer.html')
    



def logoutcustomer(request):
     auth.logout(request)
     return redirect('/customer')


def registercustomer(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
    
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                    messages.info(request,'username taken')
                    return redirect('registercustomer')
            elif User.objects.filter(email=email).exists():
                 messages.info(request,'email taken')
                 return redirect('registercustomer')
            else:
                    
                    user = User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name,email=email)
                    user.save()
                    print("usercreated")
                    return redirect('/customer/login')
        else:
            messages.info(request,'password not matching')
            return redirect('registercustomer')


    else:
        return render(request,'regsitercustomer.html')
@csrf_exempt
def addproducttocart(request):
    
        product_id = int(request.POST['product'])
        user = request.user
        cart_instance = CustomerCart(product_id = product_id,
                                    customer = user)
        cart_instance.save()
        return JsonResponse({'result':'success'})
    
@csrf_exempt
def removeproductfromcart(request):
   
        product_id = int(request.POST['product'])
        user = request.user
        cart_instance = CustomerCart.objects.filter(customer = user,product=product_id)
        cart_instance.delete()
        return JsonResponse({'result':'success'})

def cart(request):
     customercarts = CustomerCart.objects.filter(customer = request.user)
     counts = len(CustomerCart.objects.filter(customer = request.user))
     total = sum(item.product.price for item in customercarts)
     return render(request,'cart.html',{'customercarts':customercarts,'total':total,'counts':counts,'user':request.user})
def deletecart(request,id):
     customercart = CustomerCart.objects.get(pk=id)
     customercart.delete()
     return redirect('/customer/cart')
def success(request,order_id):
     order_id = order_id
     cart  = Cardorder.objects.get(razor_pay_order_id = order_id)
     cart.is_paid = True
     cart.reciept_num = str(uuid.uuid1())
     customercarts = CustomerCart.objects.filter(customer = request.user)
     customercarts.delete()
     cart.save()
     return redirect('/customer/cart')
def checkout(request):
     if request.method == 'POST':
        delivery_address = request.POST['address']
        delivery_phone = request.POST['number']
     customercarts = CustomerCart.objects.filter(customer = request.user)
     total = sum(item.product.price for item in customercarts)
     client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
     payment = client.order.create({'amount': total*100,'currency':'INR','payment_capture':0})   
     cartobj = Cardorder(razor_pay_order_id = payment['id'],customer = request.user,amount=total,delivery_address=delivery_address,delivery_phone=delivery_phone)
     cartobj.save()
     return render(request,'checkout.html',{'total':total,'payment':payment,'user':request.user})   