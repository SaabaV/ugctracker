from django import forms
from .models import Profile
from .models import ProfileCompany, Company


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'goal']
        widgets = {
            'goal': forms.Select(choices=Profile.DEAL_GOALS),
        }


class ProfileCompanyForm(forms.ModelForm):
    company_name = forms.CharField()
    company_info = forms.CharField(widget=forms.Textarea)
    company_website = forms.URLField()
    company_email = forms.EmailField()
    company_contact_person = forms.CharField()
    company_contacted_via = forms.ChoiceField(choices=Company.CONTACTED_VIA_CHOICES)
    company_niche = forms.ChoiceField(choices=Company.NICHE_CHOICES)

    class Meta:
        model = ProfileCompany
        fields = ['collaboration_status', 'deal_amount', 'content_count', 'custom_info']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.company:
            self.fields['company_name'].initial = self.instance.company.name
            self.fields['company_info'].initial = self.instance.company.info
            self.fields['company_website'].initial = self.instance.company.website
            self.fields['company_email'].initial = self.instance.company.email
            self.fields['company_contact_person'].initial = self.instance.company.contact_person
            self.fields['company_contacted_via'].initial = self.instance.company.contacted_via
            self.fields['company_niche'].initial = self.instance.company.niche

    def save(self, commit=True):
        profile_company = super().save(commit=False)
        company = profile_company.company
        company.name = self.cleaned_data['company_name']
        company.info = self.cleaned_data['company_info']
        company.website = self.cleaned_data['company_website']
        company.email = self.cleaned_data['company_email']
        company.contact_person = self.cleaned_data['company_contact_person']
        company.contacted_via = self.cleaned_data['company_contacted_via']
        company.niche = self.cleaned_data['company_niche']
        company.save()
        if commit:
            profile_company.save()
        return profile_company


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'goal']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

