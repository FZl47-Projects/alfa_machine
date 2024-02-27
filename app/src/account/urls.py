from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('reset-password', views.ResetPassword.as_view(), name='reset_password'),
    # user
    path('user/add', views.UserAdd.as_view(), name='user__add'),
    path('user/list', views.UserList.as_view(), name='user__list'),
    path('user/<int:user_id>/detail', views.UserDetail.as_view(), name='user__detail'),
    path('user/<int:user_id>/delete', views.UserDelete.as_view(), name='user__delete'),
    path('user/<int:user_id>/update', views.UserUpdate.as_view(), name='user__update'),
]
