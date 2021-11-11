from django import forms

class FilterForm(forms.Form):
    title_filter = forms.CharField(max_length=100, required=False,  
        widget=forms.TextInput( attrs={'placeholder': ' Filter..', 'class': 'form-control'}))
