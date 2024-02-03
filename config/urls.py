from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('public.urls', namespace='public')),
    path('u/', include('account.urls', namespace='account')),
    path('support/', include('support.urls', namespace='support')),
    path('notification/', include('notification.urls', namespace='notification')),

    path('dp/general/', include('departments.general.urls', namespace='dp_general')),
    path('dp/commerce/', include('departments.commerce.urls', namespace='dp_commerce')),
    path('dp/warehouse/', include('departments.warehouse.urls', namespace='dp_warehouse')),
    path('dp/control-project/', include('departments.control_project.urls', namespace='dp_control_project')),
    path('dp/control-quality/', include('departments.control_quality.urls', namespace='dp_control_quality')),
    path('dp/financial/', include('departments.financial.urls', namespace='dp_financial')),
    path('dp/technical/', include('departments.technical.urls', namespace='dp_technical')),
    path('dp/production/', include('departments.production.urls', namespace='dp_production')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'public.views.err_403_handler'
handler404 = 'public.views.err_404_handler'
handler500 = 'public.views.err_500_handler'
