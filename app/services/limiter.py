"""
Модуль налаштовує rate limiting для застосунку.

Використовується SlowAPI з ключем, що базується на IP-адресі клієнта.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Лімітер запитів за IP користувача
limiter = Limiter(key_func=get_remote_address)
