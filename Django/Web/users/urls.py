from django.urls import path
from . import views

urlpatterns = [
        path('register', views.createUserGet    ),
        path('registerpost', views.createUserPost    ),
        path('login', views.loginGet    ),
        path('loginpost', views.loginPost    ),
        path('', views.index    ),
        path('<int:id>', views.index    ),
        path('logout', views.logout    ),
        path('user', views.user    ),
        path('update_user', views.update_user    ),
        path('confirm_otp/', views.confirmOTP, name='confirm_otp'),
        path('vnpay-return', views.vnpay_return, name='vnpay_return'),

        path('add_cart/<int:id>', views.add_to_cart),
        path('cart', views.cart),
        path('except_cart/<int:id>', views.except_cart),
        path('plus_cart/<int:id>', views.add_cart),
        path('remove_cart/<int:id>', views.remove_cart),
        
        path('checkout', views.checkout),
        path('discount', views.discount),
        path('save_discount/<int:id>', views.save_discount),
        path('remove_save_discount/<int:id>', views.remove_save_discount),
        ]