from django.db import models

class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Название на русском')
    title_en = models.TextField(blank=True, verbose_name='Название на английском')
    title_ja = models.TextField(blank=True, verbose_name='Название на японском')
    image = models.ImageField(
        blank=True, default='None',
        verbose_name='Картинка'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name = 'next_evolution',
        verbose_name='Развитие'

    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE,
        null=False, verbose_name='Покемон'
    )
    lat = models.FloatField(null=True, verbose_name='Точка координат')
    lon = models.FloatField(null=True, verbose_name='Точка координат')
    appeared_at = models.DateTimeField(
        null=True,
        verbose_name='Дата появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        verbose_name='Дата исчезновения'
    )
    level = models.IntegerField(blank=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, verbose_name='Атака')
    defence = models.IntegerField(blank=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, verbose_name='Выносливость')
    def __str__(self):
        return self.pokemon.title_ru
