from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    choices = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]


class MyUser(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        null=False,
        blank=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        null=False,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Элетронная почта',
        max_length=254,
        null=False,
        blank=False,
        unique=True
    )

    avatar = models.ImageField(
        verbose_name='Фото профиля',
        help_text='Добавте фото вашего профиля.',
        upload_to='profile_images',
    )
    role = models.TextField(
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Пользовательская роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


User = get_user_model()


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='is_subscribed'
    )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"
