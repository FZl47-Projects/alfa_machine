from django.urls import path
from . import views


app_name = 'support'
urlpatterns = [
    path('ticket', views.Ticket.as_view(), name='ticket'),
    path('ticket/department', views.TicketDepartment.as_view(), name='ticket_department'),
]
