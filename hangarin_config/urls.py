"""
URL configuration for hangarin_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.http import FileResponse
from django.views.generic import TemplateView
from django.urls import path, re_path, include
from pathlib import Path
from django.conf import settings
from tasks.views import (
    DashboardView,
    HomeView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    mark_task_complete,
)


def service_worker_view(request):
    service_worker_path = Path(settings.BASE_DIR) / 'static' / 'serviceworker.js'
    return FileResponse(service_worker_path.open('rb'), content_type='application/javascript')

urlpatterns = [
    path('debug-urlconf/', TemplateView.as_view(template_name='home.html'), name='debug_urlconf'),
    path('', HomeView.as_view(), name='home'),
    path(
        'manifest.webmanifest',
        TemplateView.as_view(
            template_name='manifest.webmanifest',
            content_type='application/manifest+json',
        ),
        name='manifest',
    ),
    path(
        'serviceworker.js',
        service_worker_view,
        name='serviceworker_compat',
    ),
    path(
        'service-worker.js',
        service_worker_view,
        name='service_worker',
    ),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tasks/', TaskListView.as_view(), name='tasks'),
    re_path(r'^tasks/new/?$', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/complete/', mark_task_complete, name='task_complete'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('pwa.urls')), 
]