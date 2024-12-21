from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView
import main.views
# import main, reports
import reports.views 

app_name = 'chem'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name='home'),
    path('signin/', main.views.signin, name='signin'),
    path('logout/', main.views.logout_view, name='logout'),
    path('contact/', main.views.contact, name='contactus'),

    # """ tasks """
    path('task/new/', reports.views.create_task, name='new_task'),
    path('task/<int:pk>/', reports.views.show_task, name='show_task'),
    path('task/<int:pk>/accept/', reports.views.accept_task, name='accept_task'),
    path('task/<int:pk>/submit/', reports.views.submit_task, name='submit_task'),
    
    # ''' reports '''
    path('report/<int:task_id>/new/', reports.views.new_report, name='new_report'),
    path('report/<int:pk>/', reports.views.update_report, name='report'),
    path('report/<int:pk>/save/', reports.views.save_record, name='save_record'),
    path('report/<int:pk>/data/', reports.views.show_report, name='show_report'),
    
    
    path('dashboard/', main.views.dashboard, name='control'),
    path('requests/', main.views.new_requests, name='requests'),
    path('password-reset/', main.views.reset_password, name='password_reset'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
