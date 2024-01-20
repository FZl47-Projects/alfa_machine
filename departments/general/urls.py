from django.urls import path
from . import views

app_name = 'departments.general'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    # path('users_list', views.UsersList.as_view(), name='users_list'),
    # path('departments_list', views.DepartmentsList.as_view(), name='departments_list'),
    # path('delete_department/<int:department_id>', views.delete_department, name='delete_department'),
    # path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
]
