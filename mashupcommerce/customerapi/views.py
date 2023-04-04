from django.shortcuts import render
from django.contrib.auth import authenticate
from accounts.models import Products
from customer.models import CustomerCart
from .serializer import ProductsListSerializer
from .serializer import CustomerCartSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.status import (
     HTTP_400_BAD_REQUEST,
     HTTP_404_NOT_FOUND,
     HTTP_200_OK
)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logincustomer(request):
    username = request.data.get("username")#geting the data from the request
    password = request.data.get("password")
    if username is None or password is None: #checking wether any of the field is empty
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)#authenticating a user
    if not user: #unauthenticated user
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

    
@csrf_exempt
@api_view(["POST"])
def logoutcustomer(request):
    request.user.auth_token.delete()
    return Response({'message':'success'},status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def registercustomer(request):
    if request.method == 'POST':
            first_name =request.data.get('first_name')
            last_name = request.data.get('last_name')
            username =request.data.get('username')
            email =request.data.get('email')
            password1 = request.data.get('password1')
            
            if  User.objects.filter(username=username).exists():
                context = {'error':'Username already exists add a new one'}
                return Response(context,status = HTTP_400_BAD_REQUEST)
            else:	
                user = User.objects.create_user(username = username, 
                                                email = email, 
                                                password = password1,
                                                first_name = first_name,
                                                last_name = last_name)
                user.save()
                context = {'success':'Created user'}
                return Response(context,status = HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def listproducts(request):
    products = Products.objects.filter(is_active=1)
    if request.user:
        context = {'userid':request.user.id}
    serializer = ProductsListSerializer(products,many=True,context=context)
    return Response(serializer.data,status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def productdetails(request):
    product_id = request.data.get("product")
    product = Products.objects.get(id = product_id)
    if request.user:
        context = {'userid':request.user.id}
    serializer = ProductsListSerializer(product,context=context)
    return Response(serializer.data,status=HTTP_200_OK)
@csrf_exempt
@api_view(["POST"])
def addproductcart(request):
    product_id = int(request.data.get("product"))
    user = request.user
    cart_instance = CustomerCart(product_id = product_id,
                                customer = user)
    cart_instance.save()
    return Response({'result':'success'})
@csrf_exempt
@api_view(["POST"])
def removeproductfromcart(request):
    product_id = int(request.data.get("product"))
    user = request.user
    cart_instance = CustomerCart.objects.filter(customer = user,product=product_id)
    cart_instance.delete()
    return Response({'result':'success'})
@csrf_exempt
@api_view(["POST"])
def listcustomercart(request):
    usercart = CustomerCart.objects.filter(customer = request.user).select_related('product')
    totalprice = sum(item.product.price for item in usercart)
    cartserialized = CustomerCartSerializer(usercart,many = True)
    return Response({'cartitems':cartserialized.data,'totalprice':totalprice})