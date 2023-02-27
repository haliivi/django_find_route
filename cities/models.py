from django.db import models

__all__ = [
    'City',
]

from django.urls import reverse


class BaseModel(models.Model):
    """
    Базовый класс модели
    """
    objects = models.Manager()

    class Meta:
        abstract = True


class City(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = [
            'name',
        ]
