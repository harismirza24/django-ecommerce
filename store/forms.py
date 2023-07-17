from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from allauth.account.forms import SignupForm

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

#overriding allauth signup form:
"""class CustomsignupForm(SignupForm):
       def __init__(self, *args, **kwargs):
    # Call the init of the parent class
        super().__init__(*args, **kwargs)
        self.fields[("mobile")] = forms.CharField(required=True)
        #"Rest of your fields"
    # Put in custom signup logic
       def custom_signup(self, request, user):
        # Set the user's type from th form reponse
        user.mobile= self.cleaned_data[("mobile")]
        
      #"Rest of your fields"

        user.save()
        return user"""