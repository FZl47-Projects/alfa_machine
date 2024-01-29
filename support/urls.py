from django.urls import path
from . import views

app_name = 'support'
urlpatterns = [
    path('ticket/add', views.TicketAdd.as_view(), name='ticket__add'),
    path('ticket/list', views.TicketList.as_view(), name='ticket__list'),
]
