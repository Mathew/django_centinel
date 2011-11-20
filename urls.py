from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

from django_centinel.views import centinel_cardholder_auth_callback
from django_centinel.views import centinel_cardholder_auth_result

#forward whatever url the user has set to the callback view
urlpatterns = patterns('',
    url(r'check_callback/$',  centinel_cardholder_auth_result, name='centinel_auth_callback'),
    (r'$', centinel_cardholder_auth_callback),
)
