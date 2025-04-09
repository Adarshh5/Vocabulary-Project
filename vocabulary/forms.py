from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Word, OfflineCoaching

from django.forms.widgets import ClearableFileInput




class registrationFrom(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password (again)', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
       
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class' :'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class FilterForm(forms.ModelForm):
    part_of_speech = forms.ChoiceField(
        choices=[
            ('', '---------'), 
            ('Verb', 'Verb'),
            ('Phrasal Verb', 'Phrasal Verb'),
            ('Adjective', 'Adjective'),
            ('Noun', 'Noun'),
            ('Adverb', 'Adverb'),
            ('Prepostion', 'Prepostion'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    level = forms.ChoiceField(
        choices=[
            ('', '---------'),  
            ('Basic', 'Basic'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Word
        fields = ['part_of_speech', 'level']




class OfflineCoachingForm(forms.ModelForm):
    class Meta:
        model = OfflineCoaching
        fields = [
            "coaching_institute_name",
            "image",
            "city",
            "contact_number",
            "duration",
            "fees",
            "description"
        ]
        labels = {
            "coaching_institute_name": "Coaching Institute Name",
            "image": "Institute Image",
            "city": "City",
            "contact_number": "Contact Number",
            "duration": "Course Duration",
            "fees": "Course Fees",
            "description": "About Your Institution"
        }
        widgets = {
            "coaching_institute_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "contact_number": forms.TextInput(attrs={"class": "form-control"}),
            "duration": forms.Select(attrs={'class': 'form-control'}),
            "fees": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": ClearableFileInput(attrs={"class": "form-control-file"}),
        }
        
        





class CoachingFilterForm(forms.ModelForm):
    class Meta:
        model = OfflineCoaching
        fields = ['city', 'duration', 'fees']
        labels = {'city': 'Select City', 'duration': 'Duration', 'fees': 'Coaching Fees'}
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['city'].required = False
        self.fields['fees'].required = False
        self.fields['duration'].required = False


