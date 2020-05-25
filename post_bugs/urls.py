from django.urls import path
from post_bugs import views

urlpatterns = [
    path('', views.index, name="home"),
    path('addticket/', views.add_ticket_view),
    path('ticket/<int:id>', views.ticketview, name="ticket"),
    path('edit/<int:id>', views.editticket, name="edit"),
    path('assign/<int:id>', views.assignticket),
    path('returnticket/<int:id>', views.returnticket, name="return"),
    path('complete/<int:id>', views.completeticket, name="complete"),
    path('reopen/<int:id>', views.reopenticket, name="reopen"),
    path('invalidticket/<int:id>', views.invalidticket, name="invalid"),
    path('profile/<int:id>', views.userview),
    path('login/', views.loginview, name="login"),
    path('logout/', views.logoutview),
]
