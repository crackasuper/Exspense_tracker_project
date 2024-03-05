from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import AddMoney, UserProfile
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
from django.utils import timezone


# Create your views here.

def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render(request, 'home/login.html')

def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id = user_id)
        AddMoney = AddMoney.objects.filter(user = user).order_by('-Date')
        paginator = Paginator(AddMoney, 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'page_obj' : page_obj

        }
        return render(request, 'home/index.html', context)
    return redirect('home')

def addmoney(request):
    return redirect(request, 'home/addmoney.html')

def profile(request):
    if request.session.has_key('is_logged'):
        return render(request, 'home/profile.html')
    return redirect('/home')

def profile_edit(request, id):
    if request.session.has_key('is_loged'):
        add = User.objects.get(id = id)
        return render(request, 'home/profile/edit.html', {'add' : add})
    return redirect('/home')

def profile_update(request, id):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            user = User.objects.get(id = id)
            user.first_name = request.POST['fname']
            user.last_name = request.POST['lname']
            user.email = request.POST['email']
            user.userprofile.Savings = request.POST['Savings']
            user.userprofile.income = request.POST['income']
            user.userprofile.profession = request.POST['profession']
            user.userprofile.save()
            user.save()
            return redirect("/profile")
    return redirect("/home")

def handleSignUp(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        profession = request.POST['profession']
        Savings = request.POST['Savings']
        income = request.POST['income']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        profile = UserProfile(Savings = Savings, profession = profession, income = income)
        if request.mthod == 'POST':
            try:
                user_exists = User.objects.get(Username = request.POST['uname'])
                messages.error(request, "Username is already exists try something else!")
                return redirect('/register')
            except User.DoesNotExist:
                if len(uname) > 15:
                    messages.error(request, "username length must be less than 15 characters, Please try again!")
                    return redirect('/register')
                if not uname.isalnum():
                    messages.error(request, "Username only containe letters and numbers Please try again")
                    return redirect('/register')
                if pass1 != pass2:
                    messages.error(request, "password does not match, please try again")
                    return redirect('/register')
            user = User.objects.create_user(uname,email,pass1)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
            profile.user = user
            profile.save()
            messages.success(request, "your account has been created successfully")
            return redirect("/")
        else:
            return HttpResponse('404 - NOT FOUND')
    else:
        return redirect('/login')
    

def handleLogIn(request):
    if request.method == 'POST':
        loginuname = request.POST['loginuname']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username = loginuname, password = loginpassword)

        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.d
            request.session['user_id'] = user
            messages.success(request, "successfully logged in ")
            return redirect('/index')
        else:
            messages.error(request, "Invalid credintials please try again")
            return redirect('/')
    return HttpResponse('404 - NOT FOUND')

def handleLogOut(request):
    del request.session['is_logged']
    del request.session['user_id']  
    logout(request)
    messages.success(request, "successfully logged out!")
    return redirect('home')


def addmoney_(request):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            user_id = request.session("user_id")
            user1 = User.objects.get(id=user_id)
            addmoney_1 = AddMoney.objects.filter(user=user1).order_by('-Date')
            add_money = request.POST['add_money']
            quantity = request.POST['quantity']
            Date = request.POST['Date']
            Catagory = request.POST['Catagory']
            add = AddMoney(user = user1,add_money = add_money, quantity = quantity, Date = Date,Catagory = Catagory)
            add.save()

def books(request):
    if request.method == 'POST':
        return render(request, '/home/data.html')
    else:
        return redirect("/")








    

        



