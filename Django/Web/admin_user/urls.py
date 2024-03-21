from django.urls import path
from . import views

urlpatterns = [
        path('admin/', views.index,name='index'),
        path('admin/create', views.create_user,name='create_user'),
        path('admin/update/<int:id>', views.update_user,name='update_user'),
        path('admin/delete/<int:id>', views.delete_user,name='delete_user'),
        
        path('admin/product', views.product,name='product'),
        path('admin/create_product', views.create_product,name='create_product'),
        path('admin/update_product/<int:id>', views.update_product,name='update_product'),
        path('admin/delete_product/<int:id>', views.delete_product,name='delete_product'),
        
        path('admin/kind', views.kind,name='kind'),
        path('admin/add_kind', views.add_kind,name='create_kind'),
        path('admin/edit_kind/<int:id>', views.edit_kind,name='update_kind'),
        path('admin/delete_kind/<int:id>', views.delete_kind,name='delete_kind'),
        
        path('admin/discount', views.discount_index,name='discount'),
        path('admin/create_discount', views.create_discount,name='create_discount'),
        path('admin/update_discount/<int:id>', views.update_discount,name='update_discount'),
        path('admin/delete_discount/<int:id>', views.delete_discount,name='delete_discount'),
        
        path('admin/statistics', views.statistics,name='statistics'),
        ]