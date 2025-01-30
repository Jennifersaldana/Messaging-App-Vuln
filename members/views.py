from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def login_user(request):
    print("Starting request")
    if request.method == "POST":
        print("Method was post")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Sending to chat")
            login(request, user)
            return redirect('chat')
        else:
            #return an invalid login
            print("send backt o login_user")
            return redirect('login')
    else:
        print("rendering!")
        return render(request, 'authenticate/login_user.html', )
    
#def register_user(request):
   # if request.method == "POST":

   # else:
     #   return render(request, 'authenticate/login.html', )

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_user')  # Redirect to your login page after logout

def lockout(request):
    # Render the lockout page using the lockout.html template
    print("SENDING USER TO THE LOCKOUT PAGE")
    return render(request, 'authenticate/lockout.html')

def join(request):
    if request.method == 'POST':
        # Get data from the form
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('passwd')

        # Perform validation (you can add more checks here)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('join')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return redirect('join')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = fname
        user.last_name = lname
        user.save()

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')  # Redirect to the login page (make sure this view exists)

    return render(request, 'authenticate/join.html')  # Replace with your actual template name