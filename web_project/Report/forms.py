from .models import RepPost
from django import forms


class RepForm(forms.ModelForm):
    rep_target = forms.CharField(label="신고대상")
    rep_content = forms.CharField(widget=forms.Textarea, label="신고내용")

    class Meta:
        model = RepPost
        fields = ('rep_target', 'rep_content')
