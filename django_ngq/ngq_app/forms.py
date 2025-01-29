from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label="", widget=forms.TextInput(attrs={"id" : "url-input", "type" : "url", "autocomplete": "off", "placeholder" : "Input your valid URL here", "required" : "True"})) # max_length=?
#query = forms.CharField(label="", widget=forms.TextInput(attrs={"id" : "forminput", "autocomplete": "off"}))