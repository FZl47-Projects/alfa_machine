from django.urls import path
from . import views

app_name = 'departments.technical'
urlpatterns = [
    path('',views.Index.as_view(),name='index')
]