from django.urls import path
from . import views

app_name = 'support'
urlpatterns = [
    path('ticket/add', views.TicketAdd.as_view(), name='ticket__add'),
    path('ticket/list', views.TicketList.as_view(), name='ticket__list'),
    path('ticket/<int:ticket_id>/detail', views.TicketDetail.as_view(), name='ticket__detail'),
    path('ticket/<int:ticket_id>/delete', views.TicketDelete.as_view(), name='ticket__delete'),
    path('ticket/<int:ticket_id>/update', views.TicketUpdate.as_view(), name='ticket__update'),
]
