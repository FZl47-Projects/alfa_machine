from django.urls import path
from . import views


app_name = 'notification'

urlpatterns = [
    path('list/department', views.NotificationDepartmentList.as_view(), name='list_department')
]
