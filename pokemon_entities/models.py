from django.db import models

class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.TextField(null=True)
    title_ja = models.TextField(null=True)
    image = models.ImageField(blank=True, default='None')
    description = models.TextField(null=True)
    def __str__(self):
        return self.title_ru

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=False)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
    def __str__(self):
        return self.pokemon.title
