"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from centinel import Centinel


class CentinelClientTest(TestCase):
    def test_centinel_01(self):
        """ Pass Merchant and Transaction information """

        order_number = 1
        order_amount = 500
        currency_code = "826"
        card_number = "4000000000000002"
        card_expiry_month = "01"
        card_expiry_year = "2012"
        order_description = ""
        trans_password = "password"

        cent = Centinel(None)

        data_dict = {}
        data_dict["TransactionPwd"] = trans_password
        data_dict["Amount"] = order_amount
        data_dict["CurrencyCode"] = currency_code
        data_dict["CardNumber"] = card_number
        data_dict["CardExpMonth"] = card_expiry_month
        data_dict["CardExpYear"] = card_expiry_year
        data_dict["OrderNumber"] = order_number

        cent.client.add("MsgType", "cmpi_lookup")

        cent.create_centinel_request(data_dict)
        result = cent.client.send_request(cent.url)
        self.assertTrue(result)
        response = cent.client.response

        self.assertEqual(response['ErrorNo'], '0')
        self.assertEqual(response['ErrorDesc'], None)

    def test_centinel_01_callback(self):
        pass
