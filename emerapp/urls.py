from django.urls import path
from emerapp import views

app_name = 'emerapp'
urlpatterns = [
        path('', views.user_input, name='user_input'),
        path('user_ouput/<int:patient_id>/', views.user_ouput, name='user_ouput'),
        #path('user_ouput', views.user_ouput, name='user_ouput'),
        path('mc/', views.mc, name='mc'),
]