from django.urls import path
from post_bugs import views

urlpatterns = [
    path('', views.index, name="home"),
    path('addticket/', views.add_ticket_view)
]
