from django.urls import path
from emerapp import views

app_name = 'emerapp'
urlpatterns = [
        path('', views.user_input, name='user_input'),
        path('api/', views.api, name='api'),
        path('user_output/<int:patient_id>/', views.user_output, name='user_output'),
        path('hos_input/', views.hos_input, name='hos_input'),
        #path('mc/', views.mc, name='mc'),
]