from django.urls import path
from . import views

app_name = 'public'
urlpatterns = [
    path('error', views.Error.as_view(), name='error'),
    path('success', views.Success.as_view(), name='success'),
    path('', views.Index.as_view(), name='index'),

    path('department_detail/<int:department_id>', views.DepartmentDetail.as_view(), name='department_detail'),

    path('project', views.Project.as_view(), name='project'),
    path('project/<int:project_id>/update', views.ProjectUpdate.as_view(), name='project_update'),
    path('project/<int:project_id>/delete', views.ProjectDelete.as_view(), name='project_delete'),
    path('project/add', views.ProjectAdd.as_view(), name='project_add'),
    path('project/file', views.ProjectFile.as_view(), name='project_file'),
    path('project/<int:project_id>', views.ProjectDetail.as_view(), name='project_detail'),

    path('task', views.Task.as_view(), name='task'),
    path('task/remind/<int:task_id>', views.TaskRemind.as_view(), name='task_remind'),
    path('task/owner', views.TaskOwner.as_view(), name='task_owner'),
    path('task/owner/<int:task_id>', views.TaskOwner.as_view(), name='task_owner_detail'),
    path('task/owner/department/<int:department_id>', views.TaskOwnerDepartment.as_view(),
         name='task_owner_department'),
    path('task/list/state', views.TaskListStateUpdate.as_view(), name='task_list_state_update'),

    path('inquiry', views.Inquiry.as_view(), name='inquiry'),
    path('inquiry/<int:inquiry_id>', views.InquiryDetail.as_view(), name='inquiry_detail'),
    path('inquiry/<int:inquiry_id>/status', views.InquiryStatus.as_view(), name='inquiry_status'),
    path('inquiry/owner', views.InquiryOwner.as_view(), name='inquiry_owner'),
    path('inquiry/<int:inquiry_id>/file', views.InquiryFile.as_view(), name='inquiry_file'),
]
