Installation
============

Basic
-----

Copy the package into your python path

Add to installed apps

Syncdb (or use a south migration)

Create the success and error urls in a urls.py and point to success/error views.

Add the relevant centinel settings to your settings.py

Add a named url (corresponding to the CENTINEL_SUCCESS_URL and CENTINEL_ERROR_URL settings) to one of your urls.py.

Create two views (one for error and one for success) that your success/error urls point to.


Settings
--------

CENTINEL_PROCESSOR_ID (String) - Received from Centinel

CENTINEL_MERCHANT_ID (String) - Received from Centinel

CENTINEL_CALLBACKURL (String) - "http://callback.url"

CENTINEL_TRANSACTION_PASSWORD (String) - should be the same as the password in your Centinel Account (you set it up)

CENTINEL_DEBUG (True/False) - If True it uses the Centinel sandbox environment

CENTINEL_SUCCESS_URL (default='centinel_success') - "The name which you refer to your success url as"

CENTINEL_ERROR_URL (default='centinel_error') - "The name which you refer to your error url as"