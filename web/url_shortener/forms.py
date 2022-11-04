from django import forms

import string

string_set  = string.ascii_letters + '-1234567890'

class UrlShortenerForm(forms.ModelForm):
    def clean_name(self):
        name    = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError(
                'Name field have to be filled',
                code = 'Invalid'
            )
        if len(name) > 0 and\
            any(chr not in string_set for chr in name):
            raise forms.ValidationError(
                'Invalid name, \
                it either contain numbers or illegal character.\
                Only use alphabets and numbers and -'
            )
        return name
