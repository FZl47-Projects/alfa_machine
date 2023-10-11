from django.urls import path
from . import views

app_name = 'departments.general'
urlpatterns = [
    path('', views.Index.as_view(),name='index'),
    path('users_list', views.UsersList.as_view(),name='users_list'),
    

]
