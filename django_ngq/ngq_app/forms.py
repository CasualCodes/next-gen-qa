from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label="", widget=forms.TextInput(attrs={"id" : "url-input", "type" : "url", "autocomplete": "off", "placeholder" : "Paste a .edu, .org, or .gov URL", "required" : "True"})) # max_length=?
#query = forms.CharField(label="", widget=forms.TextInput(attrs={"id" : "forminput", "autocomplete": "off"}))