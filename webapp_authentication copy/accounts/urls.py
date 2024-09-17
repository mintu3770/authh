from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Traditional Django signup
    path('login/', views.login, name='login'),  # Traditional Django login
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard view for logged-in users
    path('logout/', views.logout, name='logout'),  # Logout view
    path('firebase-auth/', views.firebase_auth, name='firebase-auth'),  # Firebase authentication for Google sign-in
]