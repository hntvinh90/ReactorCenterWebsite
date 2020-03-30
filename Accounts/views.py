from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'html/accounts.html')

def mylogin(request):
    status = 'Có lỗi xảy ra nhưng chưa xác định được.'
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username and password:
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                status = ''
                login(request, user)
            else:
                status = 'Sai mật khẩu.'
        else:
            status = 'Tên đăng nhập không tồn tại.'
    return JsonResponse({
        'status': status
    })

def mylogout(request):
    logout(request)
    return JsonResponse({})

def change_password(request):
    status = 'Có lỗi xảy ra nhưng chưa xác định được.'
    username = request.user
    password = request.POST.get('password', '')
    new_password = request.POST.get('new_password', '')
    if username and password and new_password:
        user = User.objects.filter(username=username)
        if user:
            if authenticate(username=username, password=password):
                status = ''
                user[0].set_password(new_password)
                user[0].save()
            else:
                status = 'Sai mật khẩu hiện tại.'
        else:
            status = 'Chưa đăng nhập.'
    return JsonResponse({
        'status': status
    })
