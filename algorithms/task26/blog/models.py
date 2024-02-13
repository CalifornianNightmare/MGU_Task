from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=450)  # заголовок поста
    author = models.ForeignKey(  # Автор поста, которого выбираем в административной панели управления
        'auth.User',
        on_delete=models.CASCADE,  # Удаление поста
    )
    body = models.TextField()  # Поле нашего поста

    def __str__(self):  # Метод
        return self.title
