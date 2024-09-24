"""
URL configuration for chem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import main.views
# import main, reports
import reports.views 

app_name = 'chem'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name='home'),
    path('signin/', main.views.signin, name='signin'),

    # """ tasks """
    path('task/new/', reports.views.create_task, name='new_task'),
    path('task/<int:pk>/', reports.views.show_task, name='show_task'),
    path('task/<int:pk>/accept/', reports.views.accept_task, name='accept_task'),
    path('task/<int:pk>/submit/', reports.views.submit_task, name='submit_task'),
    
    # ''' reports '''
    path('report/new/', reports.views.new_report, name='new_report'),
    path('report/<int:pk>/', reports.views.update_report, name='report'),
    path('report/<int:pk>/save/', reports.views.save_record, name='save_record'),
    path('report/<int:pk>/data/', reports.views.show_report, name='show_report'),
    
    
    path('control/', main.views.control, name='control'),
    path('requests/', main.views.new_requests, name='requests'),
]
