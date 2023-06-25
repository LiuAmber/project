from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from app01.views.interface import login_page
from app01.models import UserInfo

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = UserInfo.objects.get(name=username, password=password)
            if user:
                return redirect('/user/list/')  # 修改重定向的 URL
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')
