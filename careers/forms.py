from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import JobSeeker, Company, Recruiter, Competence, JobOpening, \
    Expertise, Requirement


class JobSeekerRegistrationForm(UserCreationForm):
    work_experience = forms.DecimalField(max_digits=2, decimal_places=1)
    phone_number = forms.CharField(max_length=10, help_text="Contact number")

    expertise = forms.ModelMultipleChoiceField(
        queryset=Expertise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = JobSeeker
        fields = ['username', 'password1', 'password2', 'first_name',
                  'last_name', 'work_experience',
                  'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(JobSeekerRegistrationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        job_seeker = super(JobSeekerRegistrationForm, self).save(commit=False)
        job_seeker.save()

        expertise_data = self.cleaned_data['expertise']
        for expertise in expertise_data:
            Competence.objects.create(job_seeker=job_seeker,
                                      expertise=expertise)

        return job_seeker


class CompanyRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=10, help_text="Contact number")
    street = forms.CharField(max_length=100)
    district = forms.CharField(max_length=50)
    province = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=5, help_text="Postal code")

    class Meta:
        model = Company
        fields = ['username', 'password1', 'password2', 'name', 'phone_number',
                  'street', 'district', 'province', 'postal_code']


class RecruiterProfileForm(UserChangeForm):
    class Meta:
        model = Recruiter
        fields = ['username', 'first_name', 'last_name']


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['job_title', 'recruiter', 'job_function', 'job_type',
                  'required_work_experience', 'min_salary', 'max_salary']

    def __init__(self, *args, company=None, **kwargs):
        super(JobOpeningForm, self).__init__(*args, **kwargs)

        if company:
            self.fields['recruiter'].queryset = Recruiter.objects.filter(
                company_id=company
            )

        self.fields['requirements'] = forms.ModelMultipleChoiceField(
            queryset=Expertise.objects.all(),
            widget=forms.CheckboxSelectMultiple,
        )

    def save(self, commit=True):
        job_opening = super(JobOpeningForm, self).save(commit=False)
        job_opening.save()

        requirements_data = self.cleaned_data['requirements']
        for expertise in requirements_data:
            Requirement.objects.create(job_opening=job_opening,
                                       expertise=expertise)

        return job_opening


class JobOpeningUpdateForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['job_title', 'recruiter', 'job_function', 'job_type',
                  'required_work_experience', 'min_salary', 'max_salary']

    def __init__(self, *args, company=None, **kwargs):
        super(JobOpeningUpdateForm, self).__init__(*args, **kwargs)

        if company:
            self.fields['recruiter'].queryset = Recruiter.objects.filter(
                company_id=company
            )

        self.fields['requirements'] = forms.ModelMultipleChoiceField(
            queryset=Expertise.objects.all(),
            widget=forms.CheckboxSelectMultiple,
        )

        if self.instance.pk:
            existing_requirements = Requirement.objects.filter(
                job_opening=self.instance
            )
            self.fields['requirements'].initial = [req.expertise for req in
                                                   existing_requirements]

    def save(self, commit=True):
        job_opening = super(JobOpeningUpdateForm, self).save(commit=False)
        job_opening.save()

        requirements_data = self.cleaned_data['requirements']
        Requirement.objects.filter(job_opening=job_opening).delete()
        for expertise in requirements_data:
            Requirement.objects.create(job_opening=job_opening,
                                       expertise=expertise)

        return job_opening


class JobSeekerProfileForm(UserChangeForm):
    expertise = forms.ModelMultipleChoiceField(
        queryset=Expertise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = JobSeeker
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'work_experience']

    def __init__(self, *args, **kwargs):
        super(JobSeekerProfileForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            existing_competences = Competence.objects.filter(
                job_seeker=self.instance)
            self.fields['expertise'].initial = [comp.expertise for comp in
                                                existing_competences]

    def is_valid(self):
        return super(JobSeekerProfileForm, self).is_valid()

    def save(self, commit=True):
        job_seeker = super(JobSeekerProfileForm, self).save(commit)

        Competence.objects.filter(job_seeker=job_seeker).delete()

        for expertise in self.cleaned_data['expertise']:
            Competence.objects.create(job_seeker=job_seeker,
                                      expertise=expertise)

        return job_seeker


class CompanyProfileForm(UserChangeForm):
    class Meta:
        model = Company
        fields = ['username', 'name', 'phone_number', 'street', 'district',
                  'province', 'postal_code']


class RecruiterRegistrationForm(UserCreationForm):
    class Meta:
        model = Recruiter
        fields = ['username', 'password1', 'password2', 'first_name',
                  'last_name']

    def __init__(self, *args, **kwargs):
        self.company_id = kwargs.pop('company_id', None)
        super(RecruiterRegistrationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        recruiter = super(RecruiterRegistrationForm, self).save(commit=False)
        recruiter.company_id = self.company_id

        if commit:
            recruiter.save()

        return recruiter


class RecruiterUpdateForm(UserChangeForm):
    class Meta:
        model = Recruiter
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(RecruiterUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(RecruiterUpdateForm, self).save(commit=False)

        if commit:
            user.save()

        return user
