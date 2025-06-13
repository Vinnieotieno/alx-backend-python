rom django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('/')

@login_required
def conversation_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').prefetch_related('replies').only('id', 'content', 'timestamp')
    unread = Message.unread.unread_for_user(request.user)
    return render(request, 'conversation.html', {'messages': messages, 'unread': unread})