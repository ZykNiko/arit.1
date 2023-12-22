from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
	path('', views.feed, name='feed'),
	path('profile/', views.profile, name='profile'),
	path('profile/<str:username>/', views.profile, name='profile'),
	path('register/', views.register, name='register'),
	path('login/', LoginView.as_view(template_name='social/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='social/logout.html'), name='logout'),
	path('post/', views.post, name='post'),
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('conoceme/', views.Conoceme, name='conoceme'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
	path('like/<int:pk>', views.darLike, name='dar_like'),
	path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
	path('manage_messages/<str:username>/', views.manage_messages, name='manage_messages'),



	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)