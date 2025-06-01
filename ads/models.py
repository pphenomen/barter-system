from django.db import models
from django.contrib.auth.models import User

class Ad(models.Model):
    """Модель для объявлений"""
    
    CONDITION_CHOICES = [
        ('Новый', 'Новый'),
        ('Б/у', 'Б/у'),
    ]
    
    CATEGORIES = [
        ('Недвижимость', 'Недвижимость'),
        ('Транспорт', 'Транспорт'),
        ('Личные вещи', 'Личные вещи'),
        ('Электроника', 'Электроника'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение (URL из интернета)')
    category = models.CharField(max_length=100, choices=CATEGORIES, verbose_name='Категория')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name='Состояние')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ExchangeProposal(models.Model):
    """Модель для предложения обмена"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals', on_delete=models.CASCADE, verbose_name='Отправленные предложения')
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals', on_delete=models.CASCADE, verbose_name='Полученные предложения')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Обмен от {self.ad_sender} к {self.ad_receiver} — {self.status}"