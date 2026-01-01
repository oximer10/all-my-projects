from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


#РЕГИСТРАЦИR
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vlog')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('vlog')
        else:
            return render(request, 'login.html', {'error': 'Неверные данные'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

#ПОКАЗ ВСЕХ СТАТЕЙ
def article_list(request):
    articles = Article.objects.filter(is_deleted=False).order_by('-pub_date')

    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    form = MessageForm()

    deleted_articles = Article.objects.filter(is_deleted=True, author=request.user) if request.user.is_authenticated else []

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        if 'create_article' in request.POST:
            form = MessageForm(request.POST,request.FILES)
            if form.is_valid():
                msg = form.save(commit=False)
                msg.author = request.user
                msg.save()
                return redirect('vlog')


            #ИЗМЕНИТЬ СТАТЬЮ
        elif 'edit_article_id' in request.POST:
            msg = get_object_or_404(Article, id=request.POST['edit_article_id'], author=request.user)
            msg.title = request.POST.get('title', msg.title)
            msg.content = request.POST.get('content', msg.content)

            if 'image' in request.FILES:
                msg.image = request.FILES['image']

            msg.save()

            django_messages.success(request, "Статья изменена")
            return redirect('vlog')

            #УДАЛИТЬ СТАТЬЮ
        elif 'article_delete_id' in request.POST:
            msg = get_object_or_404(Article, id=request.POST['article_delete_id'], author=request.user)
            msg.is_deleted = True
            msg.save()
            django_messages.success(request, "Статья удалена")
            return redirect('vlog')

            #ВОССТАНОВИТЬ СТАТЬЮ
        elif 'article_restore_id' in request.POST:
            msg = get_object_or_404(Article, id=request.POST['article_restore_id'], author=request.user, is_deleted=True)
            msg.is_deleted = False
            msg.save()
            django_messages.success(request, "Статья восстановлена")
            return redirect('vlog')

    return render(request, 'vlog.html', {
        'page_obj': page_obj,
        'messages_list': articles,
        'deleted_articles': deleted_articles,
        'form': form
    })

@login_required
def toggle_like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('vlog')
