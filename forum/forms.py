from django import forms

class FilterForm(forms.Form):
    title_filter = forms.CharField(max_length=100, label='filter')
