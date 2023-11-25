from django.urls import path
from . import views


app_name = 'departments.warehouse'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('registrations/', views.Registration.as_view(), name='registration'),
    path('register/<int:item_id>/', views.RegisterDetail.as_view(), name='register_detail'),
]
