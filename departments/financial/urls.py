from django.urls import path
from . import views

app_name = 'departments.financial'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # payment
    path('payment/add', views.PaymentAdd.as_view(), name='payment__add'),
    path('payment/list', views.PaymentList.as_view(), name='payment__list'),
    path('payment/<int:payment_id>/detail', views.PaymentDetail.as_view(), name='payment__detail'),
    path('payment/<int:payment_id>/delete', views.PaymentDelete.as_view(), name='payment__delete'),
    path('payment/<int:payment_id>/update', views.PaymentUpdate.as_view(), name='payment__update'),
    # surety bond
    path('surety-bond/add', views.SuretyBondAdd.as_view(), name='surety_bond__add'),
    path('surety-bond/list', views.SuretyBondList.as_view(), name='surety_bond__list'),
    path('surety-bond/<int:surety_bond_id>/detail', views.SuretyBondDetail.as_view(), name='surety_bond__detail'),
    path('surety-bond/<int:surety_bond_id>/delete', views.SuretyBondDelete.as_view(), name='surety_bond__delete'),
    path('surety-bond/<int:surety_bond_id>/update', views.SuretyBondUpdate.as_view(), name='surety_bond__update'),
    # reminder
    path('reminder/add', views.ReminderAdd.as_view(), name='reminder__add'),
    path('reminder/list', views.ReminderList.as_view(), name='reminder__list'),
    path('reminder/<int:reminder_id>/delete', views.ReminderDelete.as_view(), name='reminder__delete'),

]
