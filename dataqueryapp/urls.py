from django.urls import path
import dataqueryapp.views as dataqueryapp


app_name = 'dataqueryapp'

urlpatterns = [
    path('test/', dataqueryapp.test, name='test'),
    path('similar_members/', dataqueryapp.similar_members, name='similar_members'),
    path('', dataqueryapp.main, name='main'),
    path('vk_groups_search/', dataqueryapp.vk_groups_search, name='vk_groups_search'),
]
