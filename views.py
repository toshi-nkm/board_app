from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import BordModel
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView
from django.urls import reverse_lazy

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, ' ', password )   
        except:
            return render(request, 'signup.html', {'error' : 'このユーザー名はすでに登録しています' })
        return render(request, 'signup.html', {'some': 100})
    return render(request, 'signup.html', {'some': 100}) 


def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return redirect('list')
        else:
            redirect('login')
    return render(request, 'login.html')

@login_required
def listfunc(request):
    object_list = BordModel.objects.all()
    return render(request,'list.html', {'object_list' : object_list }) 

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
    object = BordModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    object = BordModel.objects.get(pk=pk)
    object.good += 1
    object.save()
    return redirect('list')

def readfunc(request, pk):
    object = BordModel.objects.get(pk=pk)
    login_user_name = request.user.get_username()
    if login_user_name in object.readtext:
        return redirect('list')
    else:
        object.read += 1
        object.readtext = object.readtext + ' ' + login_user_name
        object.save()
        return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BordModel
    fields = ('title', 'content', 'author', 'image')
    success_url = reverse_lazy('list')

