from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import Todoform
from .models import TodoModel
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                 return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Username Taken! Choose another username'},)
        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Passwords did not Match!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
       user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
       if user is None:
          return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username and Password does not match!'}) 
       else:
           login(request,user)
           return redirect('home')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodos(request):
    if request.method == 'GET':
        return render(request,'todo/createtodos.html',{'form':Todoform()})
    else:
        try:
            form = Todoform(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/createtodos.html',{'form':Todoform(),'error':'Todo title is too long!'})

@login_required
def currenttodos(request):
    todos = TodoModel.objects.filter(user=request.user,DateCompleted__isnull=True)
    return render(request,'todo/currenttodos.html',{'todos':todos})

@login_required
def completedtodos(request):
    todos = TodoModel.objects.filter(user=request.user,DateCompleted__isnull=False).order_by('-DateCompleted')
    return render(request,'todo/completedtodos.html',{'todos':todos})

@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(TodoModel,pk=todo_pk,user=request.user)
    form = Todoform(instance=todo)
    if request.method == 'GET':
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form = Todoform(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':'Bad Data passed!'})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(TodoModel,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.DateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(TodoModel,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

