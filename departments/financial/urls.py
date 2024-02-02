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

]
