# tracker/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ElegantUserCreationForm(UserCreationForm):
    """A cleaner signup form that hides detailed password help texts."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

    class Meta:
        model = User
        fields = ("username",) # Use default fields, or add more if needed