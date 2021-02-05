from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

from django.shortcuts import render, HttpResponse
def index(request):
    if 'loggedInId' in request.session:
        context = {
            'loggedInUser': User.objects.get(id = request.session['loggedInId']),
            'items': Item.objects.all()
        }
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")

def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    else:
        errors = User.objects.loginValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/account/login")
        else:
            userswithSameemail = User.objects.filter(email = request.POST['email'])
            request.session['loggedInId'] = userswithSameemail[0].id
        return redirect("/")

def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    else:
        errors = User.objects.registerValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/account/register")
        else:
            hashPW = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hashPW, confirm_PW = hashPW)
            request.session['loggedInId'] = newUser.id
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def newItem(request):
    if request.method == 'GET':
        if 'loggedInId' in request.session:
            context = {
                'loggedInUser': User.objects.get(id = request.session['loggedInId']),
                'items': Item.objects.all()
            }
            return render(request, "newitem.html", context)
        else:
            return redirect("/account/register")
    else:
        errors = Item.objects.itemValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/item/new")
        else:
            Item.objects.create(title = request.POST['title'], description = request.POST['description'], category = request.POST['category'], condition = request.POST['condition'], price = request.POST['price'], image = request.FILES['image'], creator =  User.objects.get(id = request.session['loggedInId']))
            # addedItem.favoritor.add(User.objects.get(id=request.session['loggedInId']))
            return redirect("/")

def viewItem(request, itemId):
    if 'loggedInId' in request.session:
        context = {
            'loggedInUser': User.objects.get(id = request.session['loggedInId']),
            'Item' : Item.objects.get(id=itemId)
        }
        return render(request, "viewItem.html", context)
    else:
        return redirect("/account/register")