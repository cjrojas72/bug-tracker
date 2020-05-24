from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustUser(AbstractUser):
    role = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['role']


class Post(models.Model):
    NEW = 'NW'
    INPROGRESS = 'IP'
    DONE = 'DN'
    INVALID = 'IV'
    STATUS_OF_TICKET = [
        (NEW, 'New'),
        (INPROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid'),
    ]
    title = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(
        CustUser, on_delete=models.CASCADE, related_name='bug_created')
    status = models.CharField(
        max_length=2,
        choices=STATUS_OF_TICKET,
        default=NEW,
    )
    assigned_to = models.ForeignKey(
        CustUser, on_delete=models.CASCADE, related_name='bug_assigned', null=True, blank=True)
    completed_by = models.ForeignKey(
        CustUser, on_delete=models.CASCADE, related_name='bug_completed', null=True, blank=True)

    def __str__(self):
        return self.title
