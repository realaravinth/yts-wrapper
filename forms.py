from django import forms

class Search(forms.Form):
    query = forms.CharField(label='query', max_length=100)

