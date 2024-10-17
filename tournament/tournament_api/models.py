from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class BaseModel(models.Model): # Базовая модель
    created_at = models.DateTimeField( # Время создания
        verbose_name='Время создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField( # Последнее изменение
        verbose_name='Время последнего изменения',
        auto_now=True
    )

    class Meta:
        abstract = True


class Balance(BaseModel):
    '''
    Баланс
    '''

    amount = models.DecimalField(
        verbose_name='Количество',
        max_digits=100,
        decimal_places=2,
        default=0.00,
        blank=False,
        null=False,
    )

    def add_amount(count: int):
        ...

    def remove_balance(count: int):
        ...
    

class CustomUser(AbstractUser):
    '''
    Пользователь
    '''

    visual_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=256,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=40,
        null=True,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True,
    )
    country = models.CharField(
        verbose_name='Страна',
        max_length=100,
        null=True,
        blank=True,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=200,
        null=True,
        blank=True,
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=150,
        null=True,
        blank=True,
    )
    postcode = models.IntegerField(
        verbose_name='Почтовый индекс',
        max_length=50,
        null=True,
        blank=True,
    )
    myself = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Емэйл',
        blank=True,
        unique=True,
        null=True,
    )

    achievements = models.ManyToManyField( # Достижения TODO
        verbose_name='Достижения',
    )
    refs = models.ManyToManyField( # Рефералы TODO
        verbose_name='Реферальная система',
    )
    balance = models.ForeignKey(
        Balance,
        on_delete=models.CASCADE,
        verbose_name='Баланс человека',
        null=False,
        blank=False,
    )

    def save(self, *args, **kwargs):
        if not self.balance:
            self.balance = Balance.objects.create()  # Создаем баланс при создании пользователя
        super().save(*args, **kwargs)


class Games(BaseModel): # Игры
    '''
    Игры
    '''

    name = models.CharField( # Имя игры
        verbose_name='Имя игры',
        max_length=128,
        null=False
    )
    photo = models.FileField( # Фотография игры
        verbose_name='Фотография игры'
    )


class Tournament(BaseModel): # Турир
    '''
    Турнир
    '''

    STATUSES = (
        ('open', 'Открытый'),
        ('ongoing', 'Идёт'),
        ('finished', 'Завершён'),
        ('canceled', 'Отменённый'),
        ('moderation', 'На модерации'),
    )
    REGION = (
        ('asia', 'Азия'),
        ('europe', 'Европа'),
        ('America', 'Америка'),
    )
    RATING = (
        ('x', 'x'),
        ('xx', 'xx'),
        ('xxx', 'xxx'),
        ('xxxx', 'xxxx'),
        ('xxxxx', 'xxxxx'),
    )

    name = models.CharField( # Имя турнира
        verbose_name='Имя турнира',
        max_length=256
    )
    info = models.TextField( # Информация о турнире
        verbose_name='Информация о турнире',
        null=True
    )
    rules = models.TextField( # Правила турнира
        verbose_name='Правила',
        null=True,
    )
    tournament_id = models.BigAutoField( # Уникальное айди турнира
        verbose_name='Айди турнира',
        default=None,
        unique=True
    )
    fee = models.IntegerField( # Комиссия при вступлении - Participation fee
        verbose_name='Комиссия при вступлении',
        default=0,
        max_length=20
    )
    reward_for_kill = models.FloatField( # Награда за убийство
        verbose_name='Награда за убийство',
        default=0,
    )
    prize_found = models.BigIntegerField( # Призовой фонд
        verbose_name='Призовой пул',
        default=0
    )
    spots = models.CharField( # Колличество победителей
        verbose_name='Количество победителей',
        default=1,
        max_length=20
    )
    status = models.CharField( # Статус турнира
        verbose_name='Статус турнира',
        max_length=25,
        choices=STATUSES,
    )
    rating = models.CharField( # Рейтинг, генерируется из 5 оценок
        verbose_name='Рейтинг',
        max_length=25,
        choices=RATING,
    )
    region = models.CharField( # Регион
        verbose_name='Регион',
        max_length=25,
        choices=REGION,
    )

    # Лимиты
    min_limit = models.IntegerField( # Нижний лимит
        verbose_name='Нижний лимит',
        default=1,
        max_length=20
    )
    max_limit = models.IntegerField( # Верхний лимит
        verbose_name='Верхний лимит',
        default=1,
        max_length=20
    )
    open = models.BooleanField( # Возможность регистрации на турнир
        verbose_name='Возможность регистрации',
        default=True,           
    )

    game = models.ForeignKey( # Игра
        Games,
        verbose_name='Игра',
        on_delete=models.CASCADE,
    )
    partipications = models.ManyToManyField( # Участники
        CustomUser,
        verbose_name='Участники',
    )


    def check_partipications(self): # Проверка нижнего и верхнего числа участников
        ...


    def generate_unique_id(self): # Генерация случайного айди у турнира
        while True:
            unique_id = random.randint(100000, 999999)
            if not self._meta.objects.filter(tournament_id=unique_id).exists():
                return unique_id
    

    def save(self, *args, **kwargs): # Выполняется при сохранении
        if not self.tournament_id:
            self.tournament_id = self.generate_unique_id()
        super().save(*args, **kwargs)