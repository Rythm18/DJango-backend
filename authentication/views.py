from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from RDR import settings
from django.core.mail import send_mail

def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname=  request.POST.get('fname')
        lname=  request.POST.get('lname')
        email=  request.POST.get('email')
        pass1=  request.POST.get('pass1')
        pass2=  request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Useername already exist!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already exist!")
            return redirect('home')

        if pass1!=pass2:
            messages.error(request, "Password did not match!")
            
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,"Your Account has been successfully created.We have sent you a confirmation email,please confirm it in order to activate!")


        subject = "Welcome to MY World"
        message = "Hello" + myuser.first_name + "!! \n" + "welcome to my world!! \n Thank you for visiting the website \n We have sent you confirmation email in order to activate your account"

        from_emial = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_emial,to_list,fail_silently=True)


        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname= user.first_name
            return render(request,"authentication/index.html",{'fname':fname})

        else:
            messages.error(request,"Bad Credential")
            return redirect('home')


    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out Successfully.")
    return redirect('home')