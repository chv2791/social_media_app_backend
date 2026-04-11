from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .forms import RegisterForm
from django.contrib.auth import login
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404

#<---------------for home page------------------->
def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # this will redirect to the profile page if login is successful
        else:
            messages.error(request, "Invalid username or password.")  # display error msg
    return render(request, 'home.html')

#<---------------for profile page------------------->
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user 
            profile.save()
            return redirect('profile')  # this will rediret to the profile page after saving
    else:
        form = ProfileForm(instance=profile)  # if profile exist then pre-fill the form 

    return render(request, 'profile.html', {'form': form, 'profile': profile})

#<---------------for logout------------------->
@require_POST
def logout_view(request):
    print("Logout view called")  # Debugging
    logout(request)
    return redirect('home')



#<---------------for register------------------->
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            Profile.objects.create(user=user, username=user.username, email=user.email)
            return redirect('profile')  
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


#<---------------for search page------------------->
def search_users(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Profile.objects.filter(username__icontains=query)
    return render(request, 'search_results.html', {'query': query, 'results': results})



#<---------------for view profile------------------->
def view_profile(request, username):
    profile = Profile.objects.get(username=username)
    return render(request, 'view_profile.html', {'profile': profile})



#<---------------for post------------------->
@login_required
def timeline(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('timeline')  # or any timeline view
    else:
        form = PostForm()
    
    posts = Post.objects.all().order_by('-created_at')  # Latest posts first
    return render(request, 'timeline.html', {'form': form, 'posts': posts})



#<---------------for saving post------------------->
@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.saved_by.add(request.user)
    return redirect('timeline')

@login_required
def unsave_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.saved_by.remove(request.user)
    return redirect('timeline')

#<---------------for deleting post------------------->
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
    return redirect('timeline')
