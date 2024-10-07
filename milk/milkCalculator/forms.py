from django import forms
from .models import MilkData


class MilkForm(forms.ModelForm):
    class Meta:
        model = MilkData
        fields = ["issue_date", "qty"]
        widgets = {
          'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
          'qty': forms.TextInput(attrs={'class': 'form-control'}), 
      }
        


class YoutubeUrl(forms.Form):
    url = forms.CharField(max_length=500)
    widgets = {
          'url': forms.TextInput(attrs={'class': 'form-control'})
      }
    


class MonthsForm(forms.Form):
    FILTER_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    )

    Month = forms.ChoiceField(choices = FILTER_CHOICES)