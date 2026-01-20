from django.urls import path
from hello import views

urlpatterns = [
    path('', views.index, name='home'),
    path('users/', views.users_list, name='users_list'),
]
