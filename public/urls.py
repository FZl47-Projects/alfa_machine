from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('project',views.Project.as_view(),name='project'),
    path('project/<int:project_id>',views.ProjectDetail.as_view(),name='project_detail'),
    path('task',views.Task.as_view(),name='task'),
    path('task/owner',views.TaskOwner.as_view(),name='task_owner'),
    path('task/owner/<int:task_id>',views.TaskOwner.as_view(),name='task_owner_detail'),
    path('task/department/<int:department_id>',views.TaskDepartment.as_view(),name='task_department'),
    # path('task/<int:task_id>',views.TaskDetail.as_view(),name='task_detail'),
]