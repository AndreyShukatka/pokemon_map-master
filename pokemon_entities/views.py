import folium
import json
from django.utils.timezone import localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()
    for pokemon_entity in PokemonEntity.objects.filter(
            appeared_at__lte=localtime(),
            disappeared_at__gte=localtime()
    ):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.image.path
        )

    pokemons_on_page = []

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    requested_pokemon_entities = list(
        requested_pokemon.entities.filter(
            appeared_at__lte=localtime(),
            disappeared_at__gte=localtime()
            )
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.image.path
        )
    pokemon = {
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_ja,
        'img_url': requested_pokemon.image.url,
        'description': requested_pokemon.description
    }
    if requested_pokemon.previous_evolution:
        pokemon['previous_evolution'] = {
            'title_ru': requested_pokemon.previous_evolution.title_ru,
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': requested_pokemon.previous_evolution.image.url
        }
    next_evolutions = requested_pokemon.next_evolutions.first()
    if next_evolutions:
        pokemon['next_evolution'] = {
            'title_ru': next_evolutions.title_ru,
            'pokemon_id': next_evolutions.id,
            'img_url': next_evolutions.image.url
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
