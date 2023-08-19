from django.urls import path
from . import views

app_name = 'departments.control_project'
urlpatterns = [
    path('', views.Index.as_view(),name='index')
]
