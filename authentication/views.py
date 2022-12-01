from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from  loginsystem import settings 
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request,"authentication/index.html")

def signup(request):

     if request.method== "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request,"Username already used! Choose a different username.")
            return redirect('home')
        if User.objects.filter(email=email):  
            messages.error(request,"Email already used! Choose a different email.")
            return redirect('home')  
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request,"Passwords don't match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request,"You can't use symbols in username!")    
            return redirect('home')

            
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
    
        messages.success(request,"You have successfully created an account!!")

        subject = "Joki Login System"
        message = "Greetings" + myuser.first_name + "We have sent you a confirmation email, please confirm your email address in order to activate your account!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
    
        return redirect ('signin')
    
     return render(request,"authentication/signup.html")





def signin(request):
    if request.method== "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1) 
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,"authentication/index.html",{'fname': fname})
        else:
            messages.error(request,"Wrong Credentials!")
        
            return redirect('home') 

    return render(request,"authentication/signin.html")

def signout(request):
  logout(request)
  messages.success(request,"You have logged out!")

  return redirect('home')