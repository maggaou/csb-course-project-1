from django.dispatch import receiver
from django.contrib.auth import user_logged_in
from django.contrib.auth import user_login_failed
from reservations.models import Reservation
import logging


logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def rec_logged_in(sender, request, user, **kwargs):
    logger.info("User %s logged in", user)

@receiver(user_login_failed)
def rec_login_failed(sender, credentials, request, **kwargs):
    logger.warning("login failed attempt %s",get_ip_address(request))

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip