from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('/login',views.logincustomer,name='logincustomer'),
    path('/signup',views.registercustomer,name='registercustomer'),
    path('/logout',views.logoutcustomer,name='logoutcustomer'),
    #path('/addtocart/<int:product_id>', views.addproducttocart, name='addtocart'),
    path('/cart',views.cart,name='cart'),
    path('/deletecart/<int:id>', views.deletecart, name='deletecart'),
    path('/success/<str:order_id>',views.success,name='success'),
    path('/checkout',views.checkout,name='checkout'),
    path('addtocart', views.addproducttocart, name='addtocart'),
    path('removefromcart', views.removeproductfromcart, name='removefromcart'),
]