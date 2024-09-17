from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from firebase_admin import auth as firebase_auth, credentials, initialize_app
from django.contrib.auth.models import User

# Initialize Firebase admin SDK
cred = credentials.Certificate("path_to_your_firebase_credentials.json")
initialize_app(cred)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    # Redirect to dashboard if already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')  # Redirect to login after logout

def firebase_auth(request):
    """
    This view handles the Firebase authentication token and checks whether the user exists
    in the Django database. If not, it creates a new user.
    """
    if request.method == 'POST':
        id_token = request.POST.get('idToken', None)

        if id_token:
            try:
                # Verify the ID token sent from the client
                decoded_token = firebase_auth.verify_id_token(id_token)
                uid = decoded_token['uid']
                email = decoded_token.get('email', None)

                # Check if a user with this email already exists in Django
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    # If user does not exist, create a new one
                    user = User.objects.create_user(username=email.split('@')[0], email=email, password=User.objects.make_random_password())

                # Authenticate and log in the user
                auth_login(request, user)
                return JsonResponse({'success': True})

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
        return JsonResponse({'success': False, 'error': 'ID token not provided'}, status=400)