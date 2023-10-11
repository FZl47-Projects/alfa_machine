from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('new_user', views.NewUser.as_view(), name='new_user'),
    path('user_profile/<int:user_id>', views.UserProfile.as_view(),name='user_profile')
]
