from django.urls import path
from . import views

urlpatterns = [
 
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('manage',views.manage,name='manage'),
    path('editproduct/<int:product_id>',views.edit,name='edit'),
    path('do_edit/<int:product_id>',views.do_edit,name='do_edit'),
    path('delete/<int:product_id>',views.delete,name='delete'),
    path('manageuser',views.manageuser,name='manageuser'),
    path('change-user-status', views.changestatususer, name='changestatususer'),
    path('deleteuser/<int:user_id>',views.deleteuser,name='deleteuser'),
    path('change-product-status', views.changestatus, name='changestatus'),
    path('userview/<int:user_id>',views.userview,name='userview'),
    path('todayssalesreport', views.todayssalesreport, name='todayssalesreport')

    #path('disableproduct/<int:product_id>',views.disableproduct,name='disableproduct'),
    #path('enableproduct/<int:product_id>',views.enableproduct,name='enableproduct'),

    
    
]
