from django.shortcuts import render

import asyncio
from asgiref.sync import sync_to_async, async_to_sync


def async_view(func):
    def inner(*args, **kwargs):
        print('running async_view')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))
    return inner


# Create your views here.
'''
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from aiohttp_requests import requests
import requests as sync_requests


# my code

def async_view(func):
    def inner(*args, **kwargs):
        print('running async_view')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))
    return inner

async def sleep_print():
    await asyncio.sleep(1)
    print('sleep_print')
    return 'foo'


async def call_to_wiki(word):
    response = await requests.get('https://en.wikipedia.org/wiki/'+word)
    text = await response.text()
    return text

async def call_to_wiki_promise(word):
    loop = asyncio.get_event_loop()
    response = sync_call_to_wiki('Water')
    return await loop.run_in_executor(None, sync_call_to_wiki, word)

def sync_call_to_wiki(word):
    return sync_requests.get('https://en.wikipedia.org/wiki/'+word).text

@async_view
async def detail(request, album_id):
    promise = sleep_print()
    import time
    start = time.time()
    task1 = await call_to_wiki('Sadness')
    task2 = await call_to_wiki('Fire')
    task3 = await call_to_wiki('Mouth')
    task4 = await call_to_wiki('Father')
    task5 = await call_to_wiki('Salt')
    task6 = await call_to_wiki('Sugar')
    task7 = await call_to_wiki('Hell')
    task8 = await call_to_wiki('Caravan')
    task9 = await call_to_wiki('Moustache')
    t10 = call_to_wiki_promise('Heaven')
    tt = time.time() - start
    print('time taken: ', tt)
    start = time.time()

    sync_call_to_wiki('Sadness')
    sync_call_to_wiki('Fire')
    sync_call_to_wiki('Mouth')
    sync_call_to_wiki('Father')
    sync_call_to_wiki('Sugar')
    sync_call_to_wiki('Hell')
    sync_call_to_wiki('Caravan')
    sync_call_to_wiki('Moustache')
    tt = time.time() - start
    print('time taken: ', tt)

    return render(request, 'music/detail.html',
                {'album': album,
                    'user': user,
                    'promise': t10})

# def detail(request, album_id):
#    print('this is the detail function')
#    return detail_inner(request,album_id)


@async_view
async def favorite(request, song_id):
    await asyncio.sleep(1)
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
