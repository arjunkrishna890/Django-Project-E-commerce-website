from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Products
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from customer.models import Cardorder
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
import datetime
import csv
# Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
                if user.is_staff == 1:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request,'not a staff')
                    return redirect('/login')
        else:
            messages.info(request,'invalid credentials')
            return redirect('/login')
        
    else:    
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        is_superuser = request.POST['is_superuser']
        is_staff = request.POST['is_staff']
        

        if password1 == password2:
           if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('register')
           elif User.objects.filter(email=email).exists():
                 messages.info(request,'email taken')
                 return redirect('register')
           else:
                    user = User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name,email=email,is_superuser=is_superuser,is_staff=is_staff)
                    user.save()
                    print("usercreated")
                    return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('register')
    else:
        return render(request,'ui.html')
def checksuperuser(user):
    return user.is_superuser
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def home(request):
     return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def addproduct(request):
     if request.method == 'POST':
          product_name = request.POST['product_name']
          price = request.POST['price']
          product_description = request.POST['product_description']
          product_picture = request.FILES['product_picture']
          accounts_products = Products(product_name = product_name, 
                                        product_description = product_description,
                                        price = price,
                                        product_picture = product_picture
                                        )
          accounts_products.save()
          return redirect('/')
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def manage(request):
   products  = Products.objects.all()
   return render(request,'manage.html',{'products':products})
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def edit(request,product_id):
     product = Products.objects.get(pk=product_id)
     return render(request,'edit.html',{'product':product})
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def do_edit(request,product_id):
     product_name_new = request.POST.get("product_name_new")
     product_description_new = request.POST.get("product_description_new")
     price_new = request.POST.get("price_new")
     product_picture_new = request.FILES['product_picture_new']
     product = Products.objects.get(pk=product_id)
     product.product_picture = product_picture_new
     product.product_name = product_name_new
     product.product_description = product_description_new
     product.price = price_new

     product.save()
     return redirect('/manage')
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def delete(request,product_id):
     product = Products.objects.get(pk=product_id)
     product.delete()
     return redirect('/manage')
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def manageuser(request):
     users = User.objects.filter(is_staff = '0' , is_superuser = '0')
     return render(request,'manageuser.html',{'users':users})

#def disable(request,user_id):
     user = User.objects.get(pk=user_id)
     user.is_active = False
     user.save()
     return redirect('/manageuser')
#def enable(request,user_id):
     user = User.objects.get(pk=user_id)
     user.is_active = True
     user.save()
     return redirect('/manageuser')

@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def deleteuser(request,user_id):
     user = User.objects.get(pk=user_id)
     user.delete()
     return redirect('/manageuser')

#def disableproduct(request,product_id):
     product = Products.objects.get(pk=product_id)
     product.is_active = False
     product.save()
     return redirect('/manage')
#def enableproduct(request,product_id):
     product = Products.objects.get(pk=product_id)
     product.is_active = True
     product.save()
     return redirect('/manage')

@csrf_exempt
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def changestatususer(request):
  
        action = request.POST['action']
        user_id = int(request.POST['user_id'])
        user_instance = User.objects.get(id=user_id)
        if action == "disable":
            user_instance.is_active = 0
        else:
            user_instance.is_active = 1
        user_instance.save()
        return JsonResponse({'result':'success'})
    
@csrf_exempt
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))  
def changestatus(request):
   
        product_id = int(request.POST['product'])
        action = request.POST['action']
        product_instance = Products.objects.get(id=product_id)
        if action == "disable":
            product_instance.is_active = 0
        else:
            product_instance.is_active = 1
        product_instance.save()
        return JsonResponse({'result':'success'})
    
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def userview(request,user_id):
     users = User.objects.get(pk=user_id)
     products = Cardorder.objects.filter(customer_id = user_id , is_paid = '1')
     return render(request,'userview.html',{'users':users,'products':products})


@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def todayssalesreport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="salesreport"'+str(datetime.date.today())+'".csv"'
    writer = csv.writer(response)
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    sales = Cardorder.objects.filter(addedon__range=(today_min, today_max),is_paid = '1')
    writer.writerow(['Order_id', 'Reciept',  'Amount','Address','Phone number'])
    for sale in sales:
        writer.writerow([sale.razor_pay_order_id, sale.reciept_num,sale.amount,sale.delivery_address,sale.delivery_phone])
    return response 

     
     