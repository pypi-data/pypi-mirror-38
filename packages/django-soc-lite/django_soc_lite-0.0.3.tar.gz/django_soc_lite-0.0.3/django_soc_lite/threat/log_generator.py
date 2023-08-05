import json
import logging
from datetime import datetime
from ..logger import log
from .. import client_id as product_id, plugin_name

IP_LIST = (
    'HTTP_CF_CONNECTING_IP',
    'HTTP_X_FORWARDED_FOR', 
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
)


def send(request, event, queryString, url, d_method='input validation', description='strong attack', risk='high', impact='high risk', cwe='190'):
    userAgent = request.META['HTTP_USER_AGENT']
    for i in IP_LIST:
        if request.META.get(str(i)):
            ip = request.META.get(str(i))
            break
    if ip:
        pass
    else:
       ip = 'unknown'

    internal_data = {
        'description':description, 'cwe':cwe,
        'method':request.method, 'queryString':queryString, 'url': request.path,
        'defence_method':d_method
    }
    logging.info(
        log(
            name="attack",
            product_id=product_id,
            attacker_ip=ip,
            attack_type=event,
            user_agent=userAgent,
            plugin_type=plugin_name,
            risk=risk,
            url=url,
            attack_data=internal_data
        )
    )
