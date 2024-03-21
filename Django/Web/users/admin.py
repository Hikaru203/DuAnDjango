from django.contrib import admin
from .models import User, Product,Cart,ProductKind,Order,OrderDetail,Discount,Discount_User

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ProductKind)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Discount)
admin.site.register(Discount_User)
