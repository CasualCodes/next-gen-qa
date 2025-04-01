from django import forms

class URLForm(forms.Form):
    url = forms.CharField(label="", widget=forms.TextInput(attrs={"id" : "url-input", "type" : "url", "class" : "input-container", "autocomplete": "off", "placeholder" : "Paste a .edu, .org, or .gov URL", "required" : "True"})) # max_length=?