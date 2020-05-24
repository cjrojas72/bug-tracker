from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from post_bugs.models import CustUser, Post
from post_bugs.forms import AddPostForm
from bug_tracker.settings import AUTH_USER_MODEL


def index(request):
    new_data = Post.objects.filter(status="NW")
    inProgress_data = Post.objects.filter(status="IP")
    done_data = Post.objects.filter(status="DN")
    return render(request, 'index.html', {'new': new_data, 'in_progress': inProgress_data, 'done': done_data})


def add_ticket_view(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                title=data['title'],
                author=request.user,
                description=data['description'],
                status='NW',
                assigned_to=None,
                completed_by=None,
            )
            return HttpResponseRedirect(reverse('home'))

    form = AddPostForm()

    return render(request, 'postticket.html', {"form": form})
