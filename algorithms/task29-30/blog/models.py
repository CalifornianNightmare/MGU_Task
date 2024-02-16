from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)  # Adding pub_date field
    objects = models.Manager()

    def __str__(self):
        return self.title
