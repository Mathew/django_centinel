Usage
=====

Create the correspoding views:

Success
-------

Send these along with the card details to the payment gateway being used.

.. code-block:: python

    def centinel_success(request, order_id, secure_dict, card_details):

The secure_dict contains the information to be sent along with the card details in your request. card_details is a dict containg the information the user entered into your site to begin with which Centinel have authorised.  Use order_id to grab order information to send the amount, items etc. along with the payment request.

Error
-----

In this view you can decide to prompt for another payment type/card, informing the user their current method has been declined.

.. code-block:: python

   def centinel_paypal_pro_error(request, error):

        return render_to_response('error.html', {

        }, context_instance=RequestContext(request))

Using the django_centinel library
---------------------------------

Send the centinel object card details in a dictionary, and in a seperate one the order details, amount in pence and the ordernumber currently associated with the user's purchase.

.. code-block:: python

    # The data dictionary must contain the amount in pence.
    data_dict={
        "Amount": int(cart.total*100),
        "CurrencyCode": "826",
        "OrderNumber": order_id
    }

    #The following card details
    card_details={
        "CardNumber": "1234567891234567",
        "CardExpDate": "0812",
        "CardStartDate": "0111",
        "CardSecCode": "123",
        "CardIssue": "02"
            }

    cent = Centinel(request, centinel_paypal_pro_process, 'centinel_form.html')

    #return the response which allows centinel to take the next step.
    return cent.centinel_lookup(data_dict, card_details)
