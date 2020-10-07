from django.urls import path
from emerapp import views

app_name = 'emerapp'
urlpatterns = [
        path('', views.response, name='response'),
        path('results/', views.results, name='results'),
]