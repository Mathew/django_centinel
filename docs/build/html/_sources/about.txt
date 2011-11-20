About
=====

A django library for interacting with Cardinal Centinel.  You pass the card details in and it returns the user to the corresponding view based on the result.

This library hasn't been checked with PCI-DSS requirements, it doesn't store any card details on the server however certain requirements still need to be met, instead using hidden forms to pass the card information back to the user and hold it in their browser (while they authenticate through an i-frame)

The library also stores results and requests for Centinel Authorisation in a CentinelResponse model so we can track history of payment authorisations.