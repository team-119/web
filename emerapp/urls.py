from django.urls import path
from emerapp import views

app_name = 'emerapp'
urlpatterns = [
        path('', views.user_input, name='user_input'),
        path('user_output/<int:Patient_id>/', views.user_output, name='user_output'),
        #path('mc/', views.mc, name='mc'),
]