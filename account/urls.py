from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('reset-password', views.ResetPassword.as_view(), name='reset_password'),

    path('user/add', views.UserAdd.as_view(), name='user__add'),
    path('user/list', views.UserList.as_view(), name='user__list'),
    path('user/<int:user_id>/detail', views.UserDetail.as_view(), name='user__detail'),
    path('user/<int:user_id>/delete', views.UserDelete.as_view(), name='user__delete'),
    path('user/<int:user_id>/update', views.UserUpdate.as_view(), name='user__update'),

    # ---

    path('signup', views.SignUp.as_view(), name='signup'),
    # path('new_user', views.NewUser.as_view(), name='new_user'),
    # path('user_profile/<int:user_id>', views.UserProfile.as_view(), name='user_profile')
]
