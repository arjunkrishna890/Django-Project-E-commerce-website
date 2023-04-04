from django.urls import path
from . import views

urlpatterns = [
     
     path('', views.logincustomer, name='logincustomerapi'),
     path('/logoutcustomer', views.logoutcustomer, name='logoutcustomerapi'),
     path('/registercustomer', views.registercustomer, name='registercustomerapi'),
     path('/listproducts', views.listproducts, name='listproductsapi'),
     path('/productdetails', views.productdetails, name='productdetailsapi'),
     path('/addproductcart', views.addproductcart, name='addproductcartapi'),
     path('/removeproductfromcart', views.removeproductfromcart, name='removeproductfromcartapi'),
     path('/listcustomercart', views.listcustomercart, name='listcustomercartapi'),
     ]    