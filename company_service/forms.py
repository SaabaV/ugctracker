from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'info', 'website', 'email', 'contact_person', 'niche', 'contacted_via', 'logo']
        widgets = {
            'niche': forms.Select(choices=Company.NICHE_CHOICES),
            'contacted_via': forms.Select(choices=Company.CONTACTED_VIA_CHOICES),
        }




