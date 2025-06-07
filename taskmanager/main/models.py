from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title
            
    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'

class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание', max_length=100)
    photo = models.ImageField('Фото', upload_to='ads_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.user.username})'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

