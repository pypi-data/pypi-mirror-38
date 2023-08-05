"""Client's access verification"""
import json
import requests
import requests_cache
from django.core.cache import cache

from . import client_id, secret, verify_url

requests_cache.install_cache('response_cache', expire_after=86400)

def verify():
    """return True if valid access else False"""
    data = {'product_id': client_id, 'api_token': secret}
    cache_string = str(client_id) + str(secret)
    if cache.get(cache_string):
        if cache.get(cache_string) == 'ok':
            return True
        else:
            return False
    else:
        response = requests.post(verify_url, json=data)
        if str(response.text) == '"trial"' or str(response.text) == '"paid"':
            cache.set(cache_string, 'ok', 60)
            return True
        else:
            cache.set(cache_string, 'denied', 60)
            return False
def check():
    """False if client_id not set, else True"""
    if client_id == 'n/a' or secret == 'n/a':
        return False
    return verify()
