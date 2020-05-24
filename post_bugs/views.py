from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from post_bugs.models import CustUser, Post
from post_bugs.forms import AddPostForm, LoginForm
from bug_tracker.settings import AUTH_USER_MODEL


def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('home')))
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def index(request):
    new_data = Post.objects.filter(status="NW")
    inProgress_data = Post.objects.filter(status="IP")
    done_data = Post.objects.filter(status="DN")
    return render(request, 'index.html', {'new': new_data, 'in_progress': inProgress_data, 'done': done_data})


@login_required
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


def ticketview(request, id):
    data = Post.objects.get(id=id)
    return render(request, 'ticketview.html', {'data': data})


def userview(request, id):
    author = CustUser.objects.get(id=id)
    posts = Post.objects.filter(author=author)
    return render(request, 'userview.html', {'author': author, 'posts': posts})
