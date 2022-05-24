from email.mime import image
from urllib import request
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Post


@login_required(login_url='loginUser')
def home(request):
    user_profile = Profile.objects.get(user=request.user)
    post_content = Post.objects.all()
    context = {"user_profile":user_profile,"post_content":post_content}
    return render(request,'home.html',context)

def signup(request):
    #   偵測POST表單傳入
    if request.method == 'POST':
        # 取得表單內容
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username):
                messages.info(request, '用戶已存在')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username ,password=password)
                user.save()

                # 登入使用者導向到基本設定
                user_login = authenticate(username=username,password=password)
                login(request, user_login)

                # 創建使用者個人檔案
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, '密碼輸入不相同')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def loginUser(request):
    if request.method == 'POST':
        # 取得表單內容
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.info(request, '使用者不存在')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, '使用者或密碼不正確')


    return render(request, 'login.html')

@login_required(login_url='loginUser')
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='loginUser')
def settings(request):
    user_profile = Profile.objects.get(user=request.user) 
    
    if request.method == "POST":
        if request.FILES.get("profileimg") == None:
            # 取表單值
            profileimg = user_profile.profileimg
            about = request.POST.get("About")
            location = request.POST.get("location")
            # 更改資料庫資料
            user_profile.profileimg = profileimg
            user_profile.about = about
            user_profile.location = location
            user_profile.save()

        if request.FILES.get("profileimg") != None:
            # 取表單值
            profileimg = request.FILES.get("profileimg")
            about = request.POST.get("About")
            location = request.POST.get("location")
            # 更改資料庫資料
            user_profile.profileimg = profileimg
            user_profile.about = about
            user_profile.location = location
            user_profile.save()

        return redirect("settings")
        
    context = {"user_profile":user_profile}
    return render(request,'settings.html',context)

@login_required(login_url='loginUser')
def post(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        image = request.FILES.get("postfile")
        user = request.user.username
        caption = request.POST.get("caption")
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    
    context = {"user_profile":user_profile}
    return render(request,'post.html',context)

