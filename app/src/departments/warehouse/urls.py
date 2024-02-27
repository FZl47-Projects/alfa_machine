from django.urls import path
from . import views

app_name = 'departments.warehouse'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # item
    path('warehouse/item/add', views.ItemAdd.as_view(), name='item__add'),
    path('warehouse/item/listl', views.ItemList.as_view(), name='item__list'),
    path('warehouse/item/<int:item_id>/detail', views.ItemDetail.as_view(), name='item__detail'),
    path('warehouse/item/<int:item_id>/delete', views.ItemDelete.as_view(), name='item__delete'),
    path('warehouse/item/<int:item_id>/update', views.ItemUpdate.as_view(), name='item__update'),
    # item file
    path('warehouse/item/file/add', views.ItemFileAdd.as_view(), name='item_file__add'),
    path('warehouse/item/file/<int:item_file_id>/delete', views.ItemFileDelete.as_view(), name='item_file__delete'),

]
