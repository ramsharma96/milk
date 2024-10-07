from django.urls import path, include
from . import views


app_name = 'milk_list'

urlpatterns = [

    path('',views.index, name="home" ),
    path('milk-form/', views.save_milk_data, name="milk"),
    path('delete/<int:pk>', views.delete_milk_data, name="delete"),
    path('update/<int:pk>', views.update_milk_data, name='update'),
    path('calculate/', views.calculate_price, name='calculate'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/', views.user_logout, name='logout'),

]