# main urls.py (project-level)
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Include 'accounts' URLs
    path('', lambda request: redirect('login')),  # Redirect root to login
]