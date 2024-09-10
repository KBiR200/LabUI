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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.home, name='home'),
    path('signin/', main.views.signin),
    path('task/new/', reports.views.create_task_view, name='new_task'),
    path('report/new/', reports.views.new_report, name='new_report'),
    path('report/<int:pk>/', reports.views.update_report, name='report'),
    path('report/<int:pk>/save/', reports.views.save_record, name='save_record'),
    path('report/<int:pk>/data/', reports.views.show_report, name='show_report'),
    path('control/', main.views.admin, name='control'),
]
