from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import main.views
# import main, reports
import reports.views 
import laboratory.views 

app_name = 'chem'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name='home'),
    path('signin/', main.views.signin, name='signin'),
    path('passchange/', main.views.password_change, name='password_change'),
    path('logout/', main.views.logout_view, name='logout'),
    path('contactus/', main.views.contact, name='contactus'),
    path('teams/', main.views.teams, name='contactus'),
    path('profile/', main.views.userprofile, name='profile'),

    # """ tasks """
    path('tasks/', reports.views.tasks, name='tasks'),
    path('task/new/', reports.views.create_task15, name='new_task'),
    path('task/<int:pk>/', reports.views.show_task, name='show_task'),
    path('task/<int:pk>/update', reports.views.update_task, name='update_task'),
    path('task/<int:pk>/accept/', reports.views.accept_task, name='accept_task'),
    path('task/<int:pk>/submit/', reports.views.submit_task, name='submit_task'),
    path('task/<int:pk>/undosubmit/', reports.views.undo_task, name='undo_task'),
    path('task/<int:pk>/addcomment/', reports.views.add_comment, name='add_comment'),
    
    # ''' reports '''
    path('report/<int:task_id>/new/', reports.views.new_report, name='new_report'),
    path('report/<int:pk>/data/', reports.views.show_report, name='show_report'),
    path('report/<int:report_id>/update', reports.views.update_report, name='update_report'),
    path('report/<int:pk>/submit/', reports.views.submit_report, name='submit_report'),

    #''' laboratory '''
    path('lab/', laboratory.views.lab, name='lab'),
    path('machine/<int:pk>/view', laboratory.views.machine, name='machine_view'),
    path('machine/edit/<int:pk>/', laboratory.views.machine_edit, name='machine_edit'),
    path('machine/add', laboratory.views.machine_add, name='machine_add'),
    

    # ''' records '''
    path('reports/', reports.views.reports, name='reports'),
    path('report/<int:pk>/save/', reports.views.save_record, name='save_record'),
    path('report/<int:pk>/delete/<int:record_id>', reports.views.delete_record, name='delete_record'),
    
    # path('dashboard/', main.views.dashboard, name='control1'),
    path('dashboard15/', main.views.dashboard, name='control'),
    path('requests/', main.views.new_requests, name='requests'),
    
    # ''' errors '''
    path('404/', main.views.error_404, name='error_404'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # for static media 
