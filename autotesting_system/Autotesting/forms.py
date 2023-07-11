from django import forms


class Submission(forms.Form):
    file = forms.FileField(label="Файл")
    # code_field = forms.CharField(widget=forms.Textarea)