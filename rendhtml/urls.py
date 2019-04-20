from django.urls import path
from . import views


urlpatterns=[
    path('base/',views.base,name='base'),
    path('base1/',views.base1,name='base1'),
    path('', views.index, name='index'),
    path('logout/',views.ulogout,name='logout'),

    path('cart/', views.cart, name='cart'),
    path('detail/', views.detail, name='detail'),
    path('list/', views.list, name='list'),
    path('login/', views.ulogin, name='login'),

    path('place_order/', views.place_order, name='place_order'),
    path('register/', views.register, name='register'),
    path('user_center_info/', views.user_center_info, name='user_center_info'),
    path('user_center_order/', views.user_center_order, name='user_center_order'),
    path('del_order/<int:order_id>', views.del_order, name='del_order'),

    path('user_center_site/', views.user_center_site, name='user_center_site'),

    path('repassword/', views.repassword, name='repassword'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('add_lcart/', views.add_lcart, name='add_lcart'),

    path('del_cart/<int:foo_id>', views.del_cart, name='del_cart'),
    path('get_code/', views.get_code, name='get_code'),

    path('checksms/', views.checksms, name='checksms'),

]