from django.urls import path
import dataqueryapp.views as dataqueryapp

app_name = 'dataqueryapp'

urlpatterns = [
    path('test/', dataqueryapp.test, name='test'),
    path('', dataqueryapp.main, name='main'),
]
