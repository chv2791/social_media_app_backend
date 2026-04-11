from django.urls import path
from knox import views as knox_views
from . import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('accounts/login/', views.home, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
    path('register/', views.register, name='register'),
    path('search/', views.search_users, name='search_users'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('timeline/', views.timeline, name='timeline'),
    path('post/<int:post_id>/save/', views.save_post, name='save_post'),
    path('post/<int:post_id>/unsave/', views.unsave_post, name='unsave_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

