from logging import getLogger

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from django_centinel.forms import CardDetailsForm
from django_centinel.forms import CentinelForm
from django_centinel.models import CentinelResponse
from django_centinel.views import centinel_iframe

from django_centinel import conf
from django_centinel.centinel_client import CentinelClient

logger = getLogger('django_paypal_centinel.centinel')


class Centinel(object):
    """ Wrapper for handling Centinel Authorisation """
    form_template = ""
    error_template = ""
    success_view = None
    return_url = ""
    request = None
    url = ""

    def __init__(self, request, form_template="django_paypal_centinel/centinel_form.html/", error_template=""):
        """ Initialise the wrapper """

        self.request = request
        self.client = CentinelClient()
        #grab urls users have setup to redirect result of the transaction to.
        self.success_view = reverse(conf.SUCCESS_VIEW)
        self.error_view = reverse(conf.ERROR_VIEW)
        self.error_template = error_template
        self.form_template = form_template

        #Get the Centinel required values from settings.
        self.url = conf.URL
        self.return_url = conf.RETURN_URL
        #Add the retrieved values to the centinel client data.
        self.client.add_many({
            'ProcessorId': conf.PROCESSOR_ID,
            'MerchantId': conf.MERCHANT_ID,
            'TransactionPwd': conf.PASSWORD
        })

    def create_centinel_request(self, data_dict, card_details):
        """ Create centinel request """

        data_required_keys = (
                "Amount", "CurrencyCode",
                "OrderNumber"
                )

        card_required_keys = (
                "CardNumber", "CardExpDate"
                )

        #Check all the required names are present otherwise raise an error.
        for name in data_required_keys:
            if name not in data_dict.keys():
                raise ImproperlyConfigured("{0} is required".format(name))

        for name in card_required_keys:
            if name not in card_details.keys():
                raise ImproperlyConfigured("{0} is required".format(name))

        self.client.add_many({
            "CardExpMonth": card_details['CardExpDate'].strftime('%m'),
            "CardExpYear": card_details['CardExpDate'].year,
            "CardNumber": card_details['CardNumber'],
            "Version": "1.7",
            "TransactionType": "C"
            })

        self.order_id = data_dict['OrderNumber']

        for key, value in data_dict.iteritems():
            self.client.add(key, value)

    def centinel_lookup(self, data_dict, card_details):
        """ Create and do lookup request for centinel """
        self.card_details = card_details

        self.client.add("MsgType", "cmpi_lookup")
        self.create_centinel_request(data_dict, card_details)
        result = self.client.send_request(self.url)

        logger.debug(self.client.response)
        logger.debug(result)
        return self.centinel_lookup_response(result)

    def centinel_lookup_response(self, result):
        """ Response from centinel handler """

        if result == True:
            self.update_centinel_response_object()
            if (self.client.response['Enrolled'] == "N" or
                self.client.response['ACSUrl'] == ("U" or "N")):
                return self.return_success_view(self.client.response['TransactionId'])
            else:
                #Display the form view
                return self.return_card_form_view()
        else:
            #display the Error view
            return self.return_error_view(self)

    def return_card_form_view(self):
        """ Create and send request to merchant """
        import logging
        logger = logging.getLogger('informed.worldpay')
        logger.debug("creating form")
        logger.debug("payload: %s", self.client.response['Payload'])
        logger.debug("return url: %s", self.return_url + "%s/" % self.client.response['TransactionId'])

        forms = {}
        forms['centinel'] = CentinelForm(
                initial={
                    "PaReq": self.client.response['Payload'],
                    "TermUrl": self.return_url,
                    "MD": ""
                    }
                )

        logger.debug(self.request)
        logger

        forms['card_details'] = self.create_temp_form()
        return centinel_iframe(self.request, forms, self.client.response['ACSUrl'], self.form_template)

    def return_error_view(self, error=None):
        """ Return an error view """

        if error == None:
            error = self.client.response['ErrorDesc']

        logger.debug("returning error view")
        return self.error_view(self.request, error)

    def return_success_view(self, transaction_id):
        """ return the success view """
        cent_resp = CentinelResponse.objects.get(transaction_id=transaction_id)
        order_id = cent_resp.order_id

        ds_fields = {
                "AUTHSTATUS3DS": self.client.response.get('PAResStatus', None),
                "CAVV": self.client.response.get('Cavv', None),
                "ECI3DS": self.client.response['EciFlag'],
                "XID": self.client.response.get('Xid', None),
                }

        if self.client.response.get('Enrolled'):
            ds_fields["MPIVENDOR3DS"] = self.client.response['Enrolled']
        else:
            ds_fields["MPIVENDOR3DS"] = "N"
        return self.success_view(self.request, order_id, ds_fields, self.card_details)

    def centinel_authenticate(self, payload, transaction_id):
        """ Send authenticate request """

        self.client.add_many({
            "MsgType": "cmpi_authenticate",
            "Version": "1.7",
            "TransactionType": "C",
            "PAResPayload": payload,
            "TransactionId": transaction_id
        })
        result = self.client.send_request(self.url)
        logger.debug(self.client.response)

        self.retrieve_card_details()
        return self.centinel_authenticate_response(result, transaction_id)

    def update_centinel_response_object(self, transaction_id=None):
        """ Create or Update the centinel object associated with the order """
        enrolled = self.client.response.get('Enrolled', None)
        acs_url = self.client.response.get('ACSUrl', None)
        if transaction_id == None:
            transaction_id = self.client.response.get('TransactionId', None)

        logger.debug(self.client.response)
        logger.debug("trans_id: %s" % transaction_id)

        cent_resp, created = CentinelResponse.objects.get_or_create(pk=transaction_id)
        cent_resp.cavv = self.client.response.get('Cavv', None)
        cent_resp.xid = self.client.response.get('Xid', None)

        order_id = getattr(self, "order_id", None)
        if order_id:
            cent_resp.order_id = order_id

        if acs_url != ("U" or "N" or None):
            cent_resp.result = "waiting"
            cent_resp.eci3ds = enrolled
        else:
            if (self.client.response['SignatureVerification'] == "Y" or
                    enrolled == "N" or acs_url == ("U" or "N")):
                cent_resp.result = "passed"
            else:
                cent_resp.result = "rejected"
        cent_resp.save()

    def centinel_authenticate_response(self, result, transaction_id):
        """ Response from centinel authenticate request """
        self.update_centinel_response_object(transaction_id)
        if result == True:
            if (self.client.response['SignatureVerification'] == "Y" and
                self.client.response['PAResStatus'] != "N"):

                return self.return_success_view(transaction_id)
            else:
                return self.return_error_view(error="Sorry you are not eligible for authentication")
        else:
            return self.return_error_view("Error Authenticating")

    def create_temp_form(self):
        """ create form from card details and check validity"""

        card_details = {
                'card_no': self.card_details['CardNumber'],
                'start_date': self.card_details['CardStartDate'],
                'expiry_date': self.card_details['CardExpDate'],
                'sec_code': self.card_details['CardSecCode'],
                'issue_number': self.card_details['CardIssue'],
                'transaction_id': self.client.response['TransactionId']
                }

        form = CardDetailsForm(card_details)
        # make sure it's valid or let it raise a Validation Exception
        if form.is_valid():
            logger.debug("valid")
        else:
            logger.debug(form.errors)
        return form

    def retrieve_card_details(self):
        """ retrieve card details from instance """

        form = CardDetailsForm(self.request.POST)

        if form.is_valid():
            self.card_details = {
                'CardNumber': form.cleaned_data['card_no'],
                'CardStartDate': form.cleaned_data['start_date'],
                'CardExpDate': form.cleaned_data['expiry_date'],
                'CardSecCode': form.cleaned_data['sec_code'],
                'CardIssue': form.cleaned_data['issue_number'],
                }
            return True
        else:
            logger.debug(form.errors)
            return False
