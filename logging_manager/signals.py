#WARGING: Some settings you may be trying to make for logging may be located in settings.py sutch as loggers
from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
import logging
from axes.signals import user_locked_out

# Set up a logger for your app
logger = logging.getLogger('audit')

# Successful login signal handler
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Signal handler to log successful user logins.
    """
    logger.info(f'Successful login: User {user.username} (ID: {user.id}) logged in from IP: {request.META.get("REMOTE_ADDR")}')

# Failed login signal handler
@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """
    Signal handler to log failed login attempts.
    """
    username = credentials.get('username', 'Unknown')
    logger.warning(f'Failed login attempt: Username {username} from IP: {request.META.get("REMOTE_ADDR")}')

# User logout signal handler
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """
    Signal handler to log user logouts.
    """
    logger.info(f'User logged out: {user.username} (ID: {user.id}) from IP: {request.META.get("REMOTE_ADDR")}')