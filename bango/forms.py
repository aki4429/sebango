from django import forms

from .models import Label, Bango


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label 
        fields = ("sebango", "qty")

class UploadFileForm(forms.Form):
    # formのname 属性が 'file' になる
    file = forms.FileField(required=True, label='')


class BangoForm(forms.ModelForm):

    class Meta:
        model = Bango 
        fields = ("hcode", "se",  "shiire", "kikaku", "biko")
