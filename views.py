from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger('informed.worldpay')


@csrf_exempt
def centinel_cardholder_auth_callback(request):
    """ callback from centinel """

    return render_to_response('centinel_callback.html', {
        'pa_res': request.POST.get('PaRes'),
        }, context_instance=RequestContext(request))


def centinel_cardholder_auth_result(request, template="centinel_error.html"):
    """ Result of auth check called by centinel """
    from centinel import Centinel
    logger.debug(request.POST)
    cent = Centinel(request)
    if request.POST.get('payres') and request.POST.get('transaction_id'):
        return cent.centinel_authenticate(request.POST['payres'], request.POST['transaction_id'])
    else:
        logger.debug("returning error")
        return cent.error_view(request, "Could not authenticate")


def centinel_iframe(request, forms, auth_url, template="django_paypal_centinel/centinel_iframe.html"):
    """
    Iframe for centinel merchant auth
    """

    return render_to_response(template, {
        'centinel_form': forms['centinel'],
        'card_details_form': forms['card_details'],
        'centinel_auth_url': auth_url,
        }, context_instance=RequestContext(request))
