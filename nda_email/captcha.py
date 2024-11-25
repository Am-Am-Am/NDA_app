import json
import sys
import requests

from django.conf import settings


def get_client_ip(request):
    """получение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def yandex_captcha_validation(token, client_ip):
    if not token or len(token) == 0:
        return False
    resp = requests.get(
        "https://captcha-api.yandex.ru/validate",
        {
            "secret": settings.YACAPTCHA_SERVER,
            "token": token,
            "ip": client_ip
        },
        timeout=1
    )
    server_output = resp.content.decode()
    print(server_output)
    if resp.status_code != 200:
        print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
        return True
    return json.loads(server_output)["status"] == "ok"
