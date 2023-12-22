from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Profile, Comment, Message

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		help_texts = {k:"" for k in fields }

class PostForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': '¿Qué está pasando?'}),
        required=True
    )

    class Meta:
        model = Post
        fields = ['content', 'imagen']  
        

class ProfileForm(forms.ModelForm):
    biography = forms.CharField(
        label='Biografía',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe algo sobre ti'}),
        max_length=150,
        required=False  
    )

    class Meta:
        model = Profile
        fields = ['image', 'biography']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Escribe tu comentario...'}),
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']
        


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']