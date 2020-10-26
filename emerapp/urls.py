from django.urls import path
from emerapp import views

app_name = 'emerapp'
urlpatterns = [
        path('', views.home, name='home'),
        path('user_input/', views.user_input, name='user_input'),
        path('hos_input/', views.hos_input, name='hos_input'),
        path('user_output/<int:patient_id>/', views.user_output, name='user_output'),
]