from django.db import models
from cities.models import *
__all__ = [
    'Train',
]


class BaseModel(models.Model):
    """
    Базовый класс модели
    """
    objects = models.Manager()

    class Meta:
        abstract = True


class Train(BaseModel):
    name = models.CharField(max_length=20, unique=True, verbose_name='Номер поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        related_name='from_city_set',
        verbose_name='Из какого города',
    )
    to_city = models.ForeignKey(
        'cities.City',
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        related_name='to_city_set',
        verbose_name='В какой город',
    )

    def __str__(self):
        return f'Поезд № {self.name} из города {self.from_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = [
            'travel_time',
        ]


class TrainTest(BaseModel):
    name = models.CharField(max_length=20, unique=True, verbose_name='Номер поезда')
    from_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        related_name='from_city',
        verbose_name='Из какого города',
    )
