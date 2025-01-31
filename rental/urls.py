from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.user_home, name='user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('add_car/', views.add_car, name='add_car'),
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'),
    path('logout/', views.user_logout, name='logout'),
    path('remove_car/<int:car_id>/', views.remove_car, name='remove_car'),
    path('payment/', views.payment_page, name='payment'),
]
