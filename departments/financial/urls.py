from django.urls import path
from . import views

app_name = 'departments.financial'
urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('project/<int:project_id>',views.PaymentProject.as_view(),name='payment_project'),
    path('payment',views.Payment.as_view(),name='payment'),
    path('prepayment',views.PrePayment.as_view(),name='prepayment'),
]