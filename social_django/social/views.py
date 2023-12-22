from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommentForm, MessageForm


def feed(request):
	posts = Post.objects.all()

	context = { 'posts': posts}
	return render(request, 'social/feed.html', context)


def Conoceme(request):
	return render(request, 'social/conoceme.html',)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('feed')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'social/register.html', context)



@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Post enviado')
            return redirect('feed')
    else:
        form = PostForm()

    
    post = None 

    return render(request, 'social/post.html', {'form': form, 'likes': post.cantidad_likes() if post else 0})

@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        messages.error(request, "El post que quieres eliminar no existe")
        return redirect('feed')
    if post.user != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este post.")

    if post.imagen:
        if os.path.isfile(post.imagen.path):
            os.remove(post.imagen.path)
    post.delete()

    messages.success(request, "El post ha sido eliminado correctamente")
    return redirect('feed')


@login_required
def darLike(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('feed')






def profile(request, username=None):
	current_user = request.user
	if username and username != current_user.username:
		user = User.objects.get(username=username)
		posts = user.posts.all()
	else:
		posts = current_user.posts.all()
		user = current_user
        

	return render(request, 'social/profile.html', {'user':user, 'posts':posts})



def change_profile_picture(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profile')  # Cambia 'profile' al nombre de tu vista de perfil
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {'form': form}
    return render(request, 'social/change_profile_picture.html', context)


def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	messages.success(request, f'sigues a {username}')
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('feed')


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('feed')  # O a donde quieras redirigir después de comentar
    else:
        form = CommentForm()

    return render(request, 'social/add_comment.html', {'form': form, 'post': post})



@login_required
def manage_messages(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('manage_messages', username=username)
    else:
        form = MessageForm()

    return render(request, 'social/manage_messages.html', {'form': form, 'receiver': receiver, 'messages': messages})