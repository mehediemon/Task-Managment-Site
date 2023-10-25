from django import forms
from taskapp.models import Client

class DocumentForm(forms.ModelForm):
   
    class Meta:
        model = Client
        fields = ('name', 'description', 'document', )