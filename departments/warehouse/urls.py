from django.urls import path
from . import views

app_name = 'departments.warehouse'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('register/<int:item_id>', views.RegisterDetail.as_view(), name='register_detail'),
    path('items', views.Items.as_view(), name='items'),
    path('items/quality/pass', views.ItemsQualityPass.as_view(), name='items_quality_pass'),
    path('items/allocation/project', views.ItemsAllocationProject.as_view(), name='items_allocation_project'),
]
