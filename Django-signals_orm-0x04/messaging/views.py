from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('/')

@login_required
@cache_page(60)
def conversation_view(request):
    messages = Message.objects.filter(sender=request.user).select_related('receiver').prefetch_related('replies').only('id', 'content', 'timestamp')
    unread = Message.unread.unread_for_user(request.user)
    return render(request, 'conversation.html', {'messages': messages, 'unread': unread})