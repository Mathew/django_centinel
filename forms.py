from django import forms


class CentinelForm(forms.Form):
    """ Form for submitting payload to Cardinal Centinel """
    PaReq = forms.CharField(widget=forms.HiddenInput)
    TermUrl = forms.URLField(widget=forms.HiddenInput)
    MD = forms.CharField(max_length=50, widget=forms.HiddenInput)


class CardDetailsForm(forms.Form):
    """ Form for hiding card details

    We do this so we aren't holding card details on the server and having to
    adhere to more PCI-DSS requirements """
    card_no = forms.CharField(max_length=16, widget=forms.HiddenInput)
    start_date = forms.CharField(max_length=10, widget=forms.HiddenInput)
    expiry_date = forms.CharField(max_length=10, widget=forms.HiddenInput)
    sec_code = forms.CharField(max_length=3, widget=forms.HiddenInput)
    issue_number = forms.CharField(max_length=20, widget=forms.HiddenInput)
    transaction_id = forms.CharField(max_length=64, widget=forms.HiddenInput)
    payres = forms.CharField(widget=forms.HiddenInput, required=False)
