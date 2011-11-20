from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PROCESSOR_ID = getattr(settings, "CENTINEL_PROCESSOR_ID", None)

if PROCESSOR_ID == None:
    raise ImproperlyConfigured("Please set CENTINEL_PROC_ID in your settings.py")

MERCHANT_ID = getattr(settings, "CENTINEL_MERCHANT_ID", None)
if MERCHANT_ID == None:
    raise ImproperlyConfigured("Please set CENTINAL_MERCHANT_ID in your settings.py")

RETURN_URL = getattr(settings, "CENTINEL_CALLBACK_URL", None)
if RETURN_URL == None:
    raise ImproperlyConfigured("Please set CENTINEL_CALLBACK_URL in your settings.py")

PASSWORD = getattr(settings, "CENTINEL_TRANSACTION_PASSWORD", None)
if PASSWORD == None:
    raise ImproperlyConfigured("Please set CENTINEL_TRANSACTION_PASSWORD in your settings.py")

SUCCESS_VIEW = getattr(settings, "CENTINEL_SUCCESS_VIEW", 'centinel_success')
ERROR_VIEW = getattr(settings, "CENTINEL_ERROR_VIEW", 'centinel_error')

debug = getattr(settings, "CENTINEL_DEBUG", True)
if debug:
    URL = "https://centineltest.cardinalcommerce.com/maps/txns.asp"
else:
    URL = ""
