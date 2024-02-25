from django.urls import path
from . import views


app_name = 'department.commerce'

urlpatterns = [
    path('', views.CommerceIndex.as_view(), name='index'),
    path('procurement/', views.ProcurementCommerceIndex.as_view(), name='procurement_index'),
]
