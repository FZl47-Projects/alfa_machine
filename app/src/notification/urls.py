from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('notification/add', views.NotificationAdd.as_view(), name='notification__add'),
    path('notification/list', views.NotificationList.as_view(), name='notification__list'),
    path('notification/<int:notification_id>/detail', views.NotificationDetail.as_view(), name='notification__detail'),
    path('notification/<int:notification_id>/delete', views.NotificationDelete.as_view(), name='notification__delete'),
    path('notification/<int:notification_id>/update', views.NotificationUpdate.as_view(), name='notification__update'),
    path('notification/seen/all', views.NotificationSeenAll.as_view(), name='notification__seen_all'),
]
