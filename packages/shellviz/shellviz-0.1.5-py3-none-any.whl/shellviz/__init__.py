import urllib.request, urllib.parse, urllib.error
import json
import os
from uuid import getnode as get_mac

VERSION = '0.1.5'

class ShellvizConnectionException(Exception):
    pass

def visualize(data, id=None):

    try:
        from django.db.models import QuerySet
        from django.db.models import Model
        from django.core import serializers
    except ImportError:
        django_enabled = False
    else:
        django_enabled = True

    if django_enabled:
        if isinstance(data, Model):
            data = [data]
        elif isinstance(data, QuerySet):
            data = list(data)
        if isinstance(data, list) and len(data) and isinstance(data[0], Model):
            data = json.loads(serializers.serialize('json', data))
            data = [serialized_model['fields'] for serialized_model in data]

    shellviz_root = os.environ.get('SHELLVIZ_ROOT', 'http://localhost:3384')  # 'http://shellviz.com'
    url = '%s/visualize' % shellviz_root

    api_key = os.environ.get('SHELLVIZ_API_KEY', '')
    mac_address = get_mac() or ''

    request_dict = {
        'data': json.dumps(data),
        'apiKey': api_key,
        'macAddress': mac_address,
        'libraryLanguage': 'python',
        'libraryVersion': VERSION
    }
    request_dict.update({'id': id} if id else {})
    request_str = urllib.parse.urlencode(request_dict).encode('utf-8')

    try:
        req = urllib.request.urlopen(url, request_str)
    except urllib.error.URLError:
        raise ShellvizConnectionException('Cannot connect to shellviz client', {'SHELLVIZ_ROOT': shellviz_root})

    return req.read()
