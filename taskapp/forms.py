from django import forms
from taskapp.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        print("form")
        model = Document
        fields = ('description', 'document', )