from django.urls import path
from . import views


app_name = 'support'
urlpatterns = [
    path('ticket', views.Ticket.as_view(), name='ticket'),
    path('ticket-del/', views.DeleteTicketView.as_view(), name='delete_ticket'),
    path('ticket/department', views.TicketDepartment.as_view(), name='ticket_department'),

    path('report/list', views.ReportList.as_view(), name='report_list'),
    path('report/list/department/create', views.ReportDepartmentCreate.as_view(), name='report_department_create'),
    path('report/list/department/list', views.ReportDepartmentList.as_view(), name='report_department_list'),
]
