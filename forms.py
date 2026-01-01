from django import forms
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # хэшируем пароль
        if commit:
            user.save()
        return user


class MessageForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['title','content','image']
        widgets = {'content': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите сообщение...',
            'rows': 3,}),}

class MessageEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content']
        widgets={'content':forms.Textarea(attrs={
            "class":"form-control",
            "placeholder":"Edit your message",
            'rows':3})}
