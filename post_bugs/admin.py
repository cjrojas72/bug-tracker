from django.contrib import admin
from post_bugs.models import CustUser, Post
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustUser, UserAdmin)
admin.site.register(Post)
