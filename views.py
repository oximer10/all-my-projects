from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages as django_messages
from .models import User,Message
from .forms import UserForm,MessageForm,MessageEditForm

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            return redirect('chat')
    else:
        form = UserForm()
    return render(request,'register.html',{'form':form})

def chat(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)

    messages_list = Message.objects.filter(is_deleted=False).order_by('timestamp')
    deleted_messages = Message.objects.filter(user=user, is_deleted=True).order_by('timestamp')

    form = MessageForm()
    if request.method == 'POST':

        # 🔴 DELETE
        if 'message_delete_id' in request.POST:
            msg = Message.objects.filter(id=request.POST['message_delete_id'], user=user).first()
            if msg:
                msg.is_deleted = True
                msg.save()
                django_messages.success(request, "Сообщение успешно удалено")
            return redirect('chat')

        if 'message_restore_id' in request.POST:
            msg = Message.objects.filter(id=request.POST['message_restore_id'], user=user).first()
            if msg:
                msg.is_deleted = False
                msg.save()
                django_messages.success(request, "Сообщение восстановлено")
            return redirect('chat')

        # 🟡 EDIT
        if 'edit_message_id' in request.POST and 'message' in request.POST:
            msg = Message.objects.filter(
                id=request.POST['edit_message_id'],
                user=user
            ).first()
            if msg:
                msg.text = request.POST['message']
                msg.save()
                django_messages.success(request, "Сообщение успешно изменено")
                return redirect('chat')

        # 🟢 CREATE
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = user
            msg.save()
            return redirect('chat')

    return render(request, 'chat.html', {
        'messages_list': messages_list,
        'deleted_messages': deleted_messages,
        'form': form,
        'user': user
    })
