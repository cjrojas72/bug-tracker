from django.urls import path
from post_bugs import views

urlpatterns = [
    path('', views.index, name="home"),
    path('addticket/', views.add_ticket_view),
    path('ticket/<int:id>', views.ticketview),
    path('profile/<int:id>', views.userview),
    path('login/', views.loginview, name="login"),
    path('logout/', views.logoutview),
]
