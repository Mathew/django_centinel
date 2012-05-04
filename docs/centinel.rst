About Cardinal Centinel
=================

Scenarios
----

Centinel has various outcomes which occur at different stages in the request proces.

The main 3 are:

1) Success, with merchant authorisation
2) Success, without merchant authorisation (not available, timeouts or not supported)
3) Failure

Flow
----

Pass card info to Cardinal Centinel.

1.
If cardholder is enrolled:
    Proceed with next step
Else:
    Process transaction normally

2.
Pass cardholder to Merchant Authorisation Url (returned by cardinal in the enrollment check)

3.
When the user is returned to the site POST the payload returned to Cardinal, they check and ensure this is a valid payment check.

4.
The response returns if the user is authorised for the payment or not.

If authorised:
    Proceed with payment
Else:
    Error occured, inform user.

For further information on the process consult the paypal documentation: https://cms.paypal.com/uk/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_api_ThreeDSecure or check the centinel installation pdf supplied with the xml documentation when you have registered with Cardinal.