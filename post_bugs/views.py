from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from post_bugs.models import CustUser, Post
from post_bugs.forms import AddPostForm, LoginForm, EditForm
from bug_tracker.settings import AUTH_USER_MODEL
from django.utils import timezone, dateformat


def age(tickets):
    for ticket in tickets:
        age = timezone.now() - ticket.date
        if int(age.days) < 1:
            ticket.date = "Today"
        else:
            ticket.date = ("{} day(s)").format(age.days)
    return tickets


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


def index(request):
    if request.user.is_authenticated:
        new_data = Post.objects.filter(status="NW").order_by('-date')
        age(new_data)
        inProgress_data = Post.objects.filter(
            status="IP").order_by('-date')
        age(inProgress_data)
        done_data = Post.objects.filter(status="DN").order_by('-date')
        age(done_data)
        invalid_data = Post.objects.filter(status="IV").order_by('-date')
        age(invalid_data)

        tickets = {
            "new": new_data,
            "inP": inProgress_data,
            "done": done_data,
            "invalid": invalid_data
        }

        return render(request, 'index.html', {"tickets": tickets})
    else:
        return HttpResponseRedirect(reverse('login'))


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


@login_required
def ticketview(request, id):
    data = Post.objects.get(id=id)
    return render(request, 'ticketview.html', {'data': data})


@login_required
def editticket(request, id):
    ticket = Post.objects.get(id=id)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data["title"]
            ticket.description = data["description"]
            ticket.save()
            url = ('/ticket/{}').format(id)
            return HttpResponseRedirect(url)

    form = EditForm(initial={
        "title": ticket.title,
        "description": ticket.description
    })

    return render(request, 'edit.html', {"form": form, "ticket": ticket})


@login_required
def assignticket(request, id):
    data = Post.objects.get(id=id)
    data.status = 'IP'
    data.assigned_to = request.user
    data.save()
    url = ('/ticket/{}').format(id)
    return HttpResponseRedirect(url)


@login_required
def returnticket(request, id):
    data = Post.objects.get(id=id)
    data.status = 'NW'
    data.assigned_to = None
    data.save()
    url = ('/ticket/{}').format(id)
    return HttpResponseRedirect(url)


@login_required
def completeticket(request, id):
    data = Post.objects.get(id=id)
    data.status = 'DN'
    data.assigned_to = None
    data.completed_by = request.user
    data.save()
    url = ('/ticket/{}').format(id)
    return HttpResponseRedirect(url)


@login_required
def reopenticket(request, id):
    data = Post.objects.get(id=id)
    data.status = 'NW'
    data.assigned_to = None
    data.completed_by = None
    data.save()
    url = ('/ticket/{}').format(id)
    return HttpResponseRedirect(url)


@login_required
def invalidticket(request, id):
    data = Post.objects.get(id=id)
    data.status = 'IV'
    data.assigned_to = None
    data.completed_by = None
    data.save()
    url = ('/ticket/{}').format(id)
    return HttpResponseRedirect(url)


@login_required
def userview(request, id):
    author = CustUser.objects.get(id=id)
    posts = Post.objects.filter(author=author).order_by('-date')
    age(posts)
    in_progress = Post.objects.filter(assigned_to=author).order_by('-date')
    age(in_progress)
    completed = Post.objects.filter(completed_by=author).order_by('-date')
    age(completed)

    tickets = {
        "filed": posts,
        "inP": in_progress,
        "completed": completed,
    }

    return render(request, 'userview.html', {'tickets': tickets, 'author': author})
