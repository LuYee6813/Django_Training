from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Post,LikePost, FollowersCount
from django.db.models import Q
import random

@login_required(login_url='loginUser')
def home(request):
    q = request.GET.get('q') 
    follower_users = FollowersCount.objects.filter(follower=User.objects.get(username=request.user.username))
    user_profile = Profile.objects.get(user=request.user)
    like_post = LikePost.objects.filter(username=request.user)

    # 沒搜尋時顯示自己和追蹤的貼文和推薦使用者
    follower_users_list = []
    follower_users_list.append(request.user.username)

    for fu in follower_users:
        follower_users_list.append(fu.user) 

    post_content = Post.objects.filter(user__in=follower_users_list)
    user_content = None


    # 推薦使用者
    all_users = User.objects.values_list('username', flat=True) # 此時過濾出來的是Queryset 
    all_users_list = list(all_users)# 轉list
    suggestions_list = [x for x in all_users_list if (x not in follower_users_list)]
    random.shuffle(suggestions_list)
    
    suggestions_list_id = User.objects.filter(username__in=suggestions_list)
    suggestions_user_profile = Profile.objects.filter(user__in=suggestions_list_id)
    
    # Debug
    # print(f'所有使用者：{all_users_list}')
    # print(f'追蹤的使用者:{follower_users_list}')
    # print(f'推薦追蹤的使用者:{suggestions_list}')

    # 搜尋時
    if q != None:
        post_content = Post.objects.filter( Q(user__icontains=q) | Q(caption__icontains=q))
        user_content = Profile.objects.filter(user__username__icontains=q)
        



    context = {
        "user_profile":user_profile,
        "follower_users":follower_users,
        "post_content":post_content,
        "user_content":user_content,
        "like_post":like_post,
        "suggestions_user_profile":suggestions_user_profile[:5]
    }

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
def profile(request,username):
    user_profile = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(user=User.objects.get(username=username))

    # 貼文
    posts = Post.objects.filter(user=User.objects.get(username=username))

    # 當前目錄使用者的粉絲
    followers = FollowersCount.objects.filter(user=User.objects.get(username=username))

    # 當前目錄使用者追蹤的使用者
    users = FollowersCount.objects.filter(follower=User.objects.get(username=username))

    
    # 如果目錄使用者的粉絲有請求使用者
    if followers.filter(user=User.objects.get(username=username),follower=request.user.username):
        follow_key = True

    # 如果是瀏覽自己使用者目錄
    elif username == str(User.objects.get(username=request.user.username)):
        follow_key = "self_profile"
    
    # 請求使用者不在目錄使用者粉絲
    else:
        follow_key = False


    # 追蹤動作 追蹤or退追
    follow_action = request.POST.get("follow_action")

    if follow_action == "add":
        FollowersCount.objects.create(user=username,follower=request.user.username)
        return redirect(f'/profile/{username}')
    elif follow_action == "del":
        FollowersCount.objects.get(user=username,follower=request.user.username).delete()
        return redirect(f'/profile/{username}')
    else:
        pass 
    
    context = {
        "user_profile":user_profile,
        "profile":profile,
        "posts":posts,
        "followers":followers,
        "users":users,
        "follow_key":follow_key
    }
    return render(request, 'profile.html',context)

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
        author_img = Profile.objects.get(user=request.user)
        caption = request.POST.get("caption")
        new_post = Post.objects.create(user=user,image=image,caption=caption,author_img=author_img)
        new_post.save()
        return redirect('/')
    
    context = {"user_profile":user_profile}
    return render(request,'post.html',context)

@login_required(login_url='loginUser')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    post_status = LikePost.objects.filter(post_id=post_id, username=username).first()

    # 加到like_post列表
    if post_status == None:
        LikePost.objects.create(post_id=post_id, username=username)
        LikePost.objects.get(post_id=post_id, username=username).save()

        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_post = LikePost.objects.get(post_id=post_id, username=username)
        like_post.delete()
        
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

