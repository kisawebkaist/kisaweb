"""
WSGI config for web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

# from core.utils import housekeeping_signal

from django.core.wsgi import get_wsgi_application

# def housekeeping_handler(sig, frame):
#     from core.utils import housekeeping_signal
#     housekeeping_signal.send(sender=sig)

# signal.signal(signal.SIGUSR1, housekeeping_handler)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

application = get_wsgi_application()
