from django.urls import path
from . import views


app_name = 'departments.financial'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('project/list/', views.ProjectListView.as_view(), name='projects_list'),
    path('project/<int:project_id>', views.PaymentProject.as_view(), name='payment_project'),
    path('payment', views.Payment.as_view(), name='payment'),
    path('prepayment', views.PrePayment.as_view(), name='prepayment'),
    path('surety-bond/save/', views.SaveSuretyBondView.as_view(), name='save_surety_bond')
]
