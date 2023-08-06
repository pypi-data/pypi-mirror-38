from django import template
from threading import Thread
from asgiref.sync import async_to_sync
import re
import asyncio
from aiohttp_requests import requests
from ../views import async_view


register = template.Library()
result = {}
result['x'] = 'null'


def start_loop(promise):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result['x'] = loop.run_until_complete(promise)


@register.filter(name='await')
def await_async(promise):
    t = Thread(target=start_loop, args=(promise,))
    t.start()
    t.join()
    print(result.get('x'))
    return result.get('x')


'''


def async_view(func):
    def inner(*args, **kwargs):
        print('running async_view')
        loop = asyncio.new_event_loop()
        asycnio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))
    return inner


class CurrentTimeNode2(template.Node):
    def __init__(self, format_string, var_name):
        self.format_string = format_string
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = 'foo'
        return ''


@register.tag(name='dft')
def do_format_time(parser, token):
    tag_name, arg = token.contents.split(None, 1)
    #a = re.search(r'(.*?) as (\w+)', arg)
    format_string, var_name = ['1', 'foo']
    return CurrentTimeNode2(format_string[1:-1], var_name)


'''
