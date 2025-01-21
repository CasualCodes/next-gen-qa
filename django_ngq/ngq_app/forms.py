from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label="Enter URL", max_length=100)
