from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Group, Profile, Area, Section


class SearchForm(forms.Form):
    group = forms.ModelChoiceField(label=_('Group'), queryset=Group.objects.all(), required=False)
    area = forms.ModelChoiceField(label=_('Choose State'), queryset=Area.objects.values_list('state', flat=True).distinct(), required=True)
    county = forms.CharField(required=True, label=_('Enter County'))
    city = forms.CharField(required=True, label=_('Enter City'))
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
    
class CreateForm(forms.ModelForm):
    typeOfListing = forms.ModelChoiceField(label=_('1. Type of Listing'), queryset=Section.objects.values_list('title', flat=True))
    statelist = forms.ModelChoiceField(label=_('2. Choose State'), queryset=Area.objects.values_list('state', flat=True).distinct(), required=True)
    county = forms.CharField(required=True, label=_('2a. Enter County'))
    city = forms.CharField(required=True, label=_('2b. Enter City'))
    contractorsList = forms.ModelChoiceField(label=_('3. Contractor by Trade'), queryset=Group.objects.filter(section_id=1).values_list('title', flat=True))
    workersList = forms.ModelChoiceField(label=_('3a. Worker by Trade'), queryset=Group.objects.filter(section_id=2).values_list('title', flat=True))
    architectList = forms.ModelChoiceField(label=_('3b. Type of Architect'), queryset=Group.objects.filter(section_id=3).values_list('title', flat=True))
    engineerList = forms.ModelChoiceField(label=_('3c. Type of Engineer'), queryset=Group.objects.filter(section_id=4).values_list('title', flat=True))

    class Meta:
        model = Item
        fields = (
            'title',
            'description',
            'price',
            'is_active'
        )

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
