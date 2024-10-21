from django import forms

from .models import User, Country
import html
#from django.utils.html import unescape
            
class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        country_choices = [(country.id, html.unescape(country.name)) for country in Country.objects.all()]
        self.fields['country'].choices = country_choices
    class Meta:
        model = User
        fields = ['name', 'email', 'country', 'notification']