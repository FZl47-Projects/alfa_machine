from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    # project
    path('project/add', views.ProjectAdd.as_view(), name='project__add'),
    path('project/list', views.ProjectList.as_view(), name='project__list'),
    path('project/<int:project_id>/detail', views.ProjectDetail.as_view(), name='project__detail'),
    path('project/<int:project_id>/delete', views.ProjectDelete.as_view(), name='project__delete'),
    path('project/<int:project_id>/update', views.ProjectUpdate.as_view(), name='project__update'),
    # project note
    path('project/note/add', views.ProjectNoteAdd.as_view(), name='project_note__add'),
    path('project/note/<int:note_id>/delete', views.ProjectNoteDelete.as_view(), name='project_note__delete'),
    # project comment
    path('project/comment/add', views.ProjectCommentAdd.as_view(), name='project_comment__add'),
    path('project/comment/<int:comment_id>/delete', views.ProjectCommentDelete.as_view(), name='project_comment__delete'),
    # project step
    path('project/step/add', views.ProjectStepAdd.as_view(), name='project_step__add'),
    path('project/step/<int:step_id>/detail', views.ProjectStepDetail.as_view(), name='project_step__detail'),
    path('project/step/<int:step_id>/delete', views.ProjectStepDelete.as_view(), name='project_step__delete'),
    path('project/step/<int:step_id>/update', views.ProjectStepUpdate.as_view(), name='project_step__update'),
    # task
    path('task/add', views.TaskAdd.as_view(), name='task__add'),
    path('task/list', views.TaskList.as_view(), name='task__list'),
    path('task/<int:task_id>/detail', views.TaskDetail.as_view(), name='task__detail'),
    path('task/<int:task_id>/delete', views.TaskDelete.as_view(), name='task__delete'),
    path('task/<int:task_id>/update', views.TaskUpdate.as_view(), name='task__update'),
    path('task/<int:task_id>/remind', views.TaskRemind.as_view(), name='task__remind'),
    # task status
    path('task/<int:task_id>/status/add', views.TaskStatusAdd.as_view(), name='task_status__add'),
    # inquiry
    path('inquiry/add', views.InquiryAdd.as_view(), name='inquiry__add'),
    path('inquiry/list', views.InquiryList.as_view(), name='inquiry__list'),
    path('inquiry/<int:inquiry_id>/detail', views.InquiryDetail.as_view(), name='inquiry__detail'),
    path('inquiry/<int:inquiry_id>/delete', views.InquiryDelete.as_view(), name='inquiry__delete'),
    path('inquiry/<int:inquiry_id>/update', views.InquiryUpdate.as_view(), name='inquiry__update'),
    # inquiry status
    path('inquiry/<int:inquiry_id>/status/modify', views.InquiryStatusModify.as_view(), name='inquiry_status__modify'),
    # inquiry file
    path('inquiry/<int:inquiry_id>/file/add', views.InquiryFileAdd.as_view(), name='inquiry_file__add'),
    path('inquiry/<int:inquiry_id>/file/<int:inquiry_file_id>/delete', views.InquiryFileDelete.as_view(),
         name='inquiry_file__delete'),
    # task masters
    path('taskmaster/add', views.TaskMasterAdd.as_view(), name='task_master__add'),
    path('taskmaster/list', views.TaskMasterList.as_view(), name='task_master__list'),
    path('taskmaster/<int:task_master_id>/detail', views.TaskMasterDetail.as_view(), name='task_master__detail'),
    path('taskmaster/<int:task_master_id>/delete', views.TaskMasterDelete.as_view(), name='task_master__delete'),
    path('taskmaster/<int:task_master_id>/update', views.TaskMasterUpdate.as_view(), name='task_master__update'),
    # departments
    path('department/add', views.DepartmentAdd.as_view(), name='department__add'),
    path('department/list', views.DepartmentList.as_view(), name='department__list'),
    path('department/<int:department_id>/detail', views.DepartmentDetail.as_view(), name='department__detail'),
    path('department/<int:department_id>/delete', views.DepartmentDelete.as_view(), name='department__delete'),
    path('department/<int:department_id>/update', views.DepartmentUpdate.as_view(), name='department__update'),
    # project files
    path('project/file/add', views.ProjectFileAdd.as_view(), name='project_file__add'),
    path('project/file/list', views.ProjectFileList.as_view(), name='project_file__list'),
    path('project/file/<int:project_file_id>/detail', views.ProjectFileDetail.as_view(), name='project_file__detail'),
    path('project/file/<int:project_file_id>/delete', views.ProjectFileDelete.as_view(), name='project_file__delete'),

    path('', views.Index.as_view(), name='index'),
]
