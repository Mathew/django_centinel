from django.db import models


class CentinelResponse(models.Model):
    """ Model for holding transaction information from Centinel

    Added to allow tracking of declines/accepts and points of failure.
    """

    STATUS_CHOICES = (
            ("waiting", "waiting"),
            ("rejected", "rejected"),
            ("passed", "passed"),
           )

    transaction_id = models.CharField(max_length=30, unique=True, primary_key=True)
    transaction_provider = models.CharField(max_length=50, blank=True, null=True)
    order_id = models.CharField(max_length=30)
    cavv = models.CharField(max_length=30, blank=True, null=True)
    eci3ds = models.NullBooleanField()
    xid = models.CharField(max_length=30, blank=True, null=True)
    auth_status_3ds = models.CharField(max_length=30)
    mpi_vendor_3ds = models.NullBooleanField()
    result = models.CharField(max_length=10, choices=STATUS_CHOICES)
