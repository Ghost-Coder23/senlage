from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
