from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Group, Profile, Area


class SearchForm(forms.Form):
    group = forms.ModelChoiceField(label=_('Group'), queryset=Group.objects.all(), required=False)
    area = forms.ModelChoiceField(label=_('Choose State'), queryset=Area.objects.values_list('state', flat=True).distinct(), required=True)
    county = forms.CharField(required=True, label=_('County'))
    city = forms.CharField(required=True, label=_('City'))
    q = forms.CharField(required=False, label=_('Description'))
    
    def filter_by(self):
        # TODO search using more than one field
        # TODO split query string and make seaprate search by words
        filters = {}
        if self.cleaned_data['group']:
            filters['group'] = self.cleaned_data['group']

        if self.cleaned_data['area']:
            filters['area'] = self.cleaned_data['area']

        filters['description__icontains'] = self.cleaned_data['q']

        return filters


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'area',
            'group',
            'state',
            'county',
            'city',
            'description',
            'price',
            'is_active'
        )

        
class EmailWidget(forms.TextInput):
    input_type = 'email'

class PhoneWidget(forms.TextInput):
    input_type = 'phone'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'email',
            'phone',
        )
        widgets = {
            'email': EmailWidget,
            'phone': PhoneWidget
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = (
            'phone',
        )
        widgets = {
            'phone': PhoneWidget
        }
