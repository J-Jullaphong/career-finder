from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import JobSeekerRegistrationForm, CompanyRegistrationForm, \
    JobSeekerProfileForm, RecruiterRegistrationForm, JobOpeningForm, \
    RecruiterProfileForm, CompanyProfileForm, \
    JobOpeningUpdateForm, RecruiterUpdateForm
from .models import JobSeeker, Company, JobOpening, JobFunction, Recruiter, \
    JobApplication, Expertise


def homepage(request):
    return render(request, 'careers/homepage.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('careers:homepage')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'careers/login.html')


def custom_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('careers:homepage')


class JobSeekerRegistrationView(CreateView):
    model = JobSeeker
    form_class = JobSeekerRegistrationForm
    template_name = 'careers/job_seeker_register.html'
    success_url = reverse_lazy('careers:homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CompanyRegistrationView(CreateView):
    model = Company
    form_class = CompanyRegistrationForm
    template_name = 'careers/company_register.html'
    success_url = reverse_lazy('careers:homepage')


def job_search(request):
    query = request.GET.get('q')
    job_function = request.GET.get('job_function')
    company_name = request.GET.get('company_name')
    required_experience = request.GET.get('required_experience')
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')
    expertise = request.GET.get('expertise')

    all_job_functions = JobFunction.objects.all()
    all_expertise = Expertise.objects.all()

    search_criteria = Q()

    if query:
        search_criteria &= Q(job_title__icontains=query)
    if job_function:
        search_criteria &= Q(job_function__function__icontains=job_function)
    if company_name:
        search_criteria &= Q(
            recruiter__company_id__name__icontains=company_name)
    if required_experience:
        search_criteria &= Q(required_work_experience__lte=required_experience)
    if min_salary:
        search_criteria &= Q(min_salary__gte=min_salary)
    if max_salary:
        search_criteria &= Q(max_salary__lte=max_salary)
    if expertise:
        search_criteria &= Q(
            requirement__expertise__skill__icontains=expertise)

    if min_salary and max_salary:
        search_criteria &= Q(min_salary__range=(min_salary, max_salary))

    job_openings = JobOpening.objects.filter(search_criteria).distinct()

    applied_job_opening_ids = set()

    if request.user.is_authenticated and hasattr(request.user, 'jobseeker'):
        applied_job_opening_ids = set(
            application.job_opening.job_opening_id
            for application in request.user.jobseeker.jobapplication_set.all()
        )
        job_openings = job_openings.exclude(pk__in=applied_job_opening_ids)

    context = {
        'job_openings': job_openings,
        'query': query,
        'job_function': job_function,
        'company_name': company_name,
        'required_experience': required_experience,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'expertise': expertise,
        'all_job_functions': all_job_functions,
        'all_expertise': all_expertise,
    }

    if request.user.is_authenticated:
        if hasattr(request.user, 'jobseeker'):
            context['applied_job_opening_ids'] = applied_job_opening_ids

    return render(request, 'careers/job_search.html', context)


def recruiter_registration_view(request, company_id):
    template_name = 'careers/recruiter_register.html'
    success_url = reverse_lazy('careers:homepage')

    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            company = Company.objects.get(company_id=company_id)
            recruiter = form.save(commit=False)
            recruiter.company_id = company
            recruiter.save()
            return redirect(success_url)
    else:
        form = RecruiterRegistrationForm()

    context = {
        'form': form,
        'company_id': company_id,
    }

    return render(request, template_name, context)


@method_decorator(login_required, name='dispatch')
class JobSeekerProfileView(View):
    template_name = 'careers/job_seeker_profile.html'

    def get(self, request, job_seeker_id):
        job_seeker = get_object_or_404(JobSeeker, job_seeker_id=job_seeker_id)
        form = JobSeekerProfileForm(instance=job_seeker)
        return render(request, self.template_name, {
            'job_seeker': job_seeker,
            'form': form,
        })

    def post(self, request, job_seeker_id):
        job_seeker = get_object_or_404(JobSeeker, job_seeker_id=job_seeker_id)
        form = JobSeekerProfileForm(request.POST, instance=job_seeker)

        if form.is_valid():
            form.save()
            return redirect('careers:job_seeker_profile',
                            job_seeker_id=job_seeker.job_seeker_id)

        return render(request, self.template_name, {
            'job_seeker': job_seeker,
            'form': form,
        })


@method_decorator(login_required, name='dispatch')
class CompanyProfileView(View):
    template_name = 'careers/company_profile.html'

    def get(self, request, company_id):
        company = get_object_or_404(Company, company_id=company_id)
        form = CompanyProfileForm(instance=company)
        return render(request, self.template_name,
                      {'company': company, 'form': form})

    def post(self, request, company_id):
        company = get_object_or_404(Company, company_id=company_id)
        form = CompanyProfileForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
        return render(request, self.template_name,
                      {'company': company, 'form': form})


@method_decorator(login_required, name='dispatch')
class RecruiterProfileView(View):
    template_name = 'careers/recruiter_profile.html'

    def get(self, request, recruiter_id):
        recruiter = get_object_or_404(Recruiter, recruiter_id=recruiter_id)
        form = RecruiterProfileForm(instance=recruiter)
        return render(request, self.template_name,
                      {'recruiter': recruiter, 'form': form})

    def post(self, request, recruiter_id):
        recruiter = get_object_or_404(Recruiter, recruiter_id=recruiter_id)
        form = RecruiterProfileForm(request.POST, instance=recruiter)
        if form.is_valid():
            form.save()
        return render(request, self.template_name,
                      {'recruiter': recruiter, 'form': form})


@login_required
def update_job_description(request, job_opening_id, company_id):
    job_opening = get_object_or_404(JobOpening, pk=job_opening_id)

    if request.user.is_authenticated:
        if hasattr(request.user, 'jobseeker'):
            return redirect('careers:homepage')
        elif hasattr(request.user, 'recruiter'):
            return redirect('careers:homepage')

    if request.method == 'POST':
        form = JobOpeningUpdateForm(request.POST, instance=job_opening,
                                    company=company_id)
        if form.is_valid():
            form.save()
            return redirect('careers:manage_job_openings',
                            company_id=company_id)
    else:
        form = JobOpeningUpdateForm(instance=job_opening, company=company_id)

    return render(request, 'careers/update_job_description.html',
                  {'form': form, 'job_opening': job_opening})


@login_required
def delete_job_opening(request, job_opening_id, company_id):
    job_opening = get_object_or_404(JobOpening, pk=job_opening_id)

    if job_opening.recruiter.company_id.user_ptr != request.user:
        return redirect('careers:homepage')

    if request.method == 'POST':
        job_opening.delete()
        return redirect('careers:manage_job_openings', company_id=company_id)

    return render(request, 'careers/delete_job_opening.html',
                  {'job_opening': job_opening})


@login_required
def manage_job_openings(request, company_id):
    user = request.user
    job_openings = None

    if user is not None and user.is_authenticated:
        if hasattr(request.user, 'jobseeker'):
            return redirect('careers:job_seeker_profile',
                            job_seeker_id=user.jobseeker.job_seeker_id)
        elif hasattr(request.user, 'recruiter'):
            job_openings = JobOpening.objects.filter(
                recruiter_id=user.recruiter.recruiter_id)
        elif hasattr(request.user, 'company'):
            job_openings = JobOpening.objects.filter(
                recruiter_id__company_id=user.company.company_id)
    else:
        messages.error(request, 'Invalid login credentials.')
        return redirect(request, 'careers:homepage')

    print("User:", user)
    print("Job Openings:", job_openings)

    return render(request, 'careers/manage_job_openings.html',
                  {'job_openings': job_openings})


class CompanyRecruiterManagementView(View):
    template_name = 'careers/company_recruiter_management.html'

    def get(self, request, **kwargs):
        company = request.user.company
        recruiters = Recruiter.objects.filter(company_id=company.company_id)
        return render(request, self.template_name, {'recruiters': recruiters})


@login_required
def post_job_opening(request, company_id):
    recruiters = Recruiter.objects.filter(company_id=request.user.company)

    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        form.fields['recruiter'].queryset = recruiters
        if form.is_valid():
            form.save()
            return redirect('careers:homepage')
    else:
        form = JobOpeningForm(company=request.user.company)
        form.fields['recruiter'].queryset = recruiters

    return render(request, 'careers/company_post.html', {'form': form})


@login_required
def apply(request, job_opening_id):
    try:
        job_seeker = get_object_or_404(JobSeeker,
                                       pk=request.user.jobseeker.job_seeker_id)

        job_opening = get_object_or_404(JobOpening, pk=job_opening_id)

        if JobApplication.objects.filter(job_opening=job_opening,
                                         job_seeker=job_seeker).exists():
            messages.warning(request, 'You have already applied for this job.')
        else:
            application = JobApplication(job_seeker=job_seeker,
                                         job_opening=job_opening)
            application.save()

            messages.success(request, 'Application submitted successfully!')

    except Exception as e:
        messages.error(request, f'Error submitting application: {str(e)}')

    return redirect('careers:job_search')


@login_required
def delete_application(request, job_opening_id):
    try:
        job_seeker = get_object_or_404(JobSeeker,
                                       pk=request.user.jobseeker.job_seeker_id)

        job_opening = get_object_or_404(JobOpening, pk=job_opening_id)

        if JobApplication.objects.filter(job_opening=job_opening,
                                         job_seeker=job_seeker).exists():
            application = JobApplication.objects.get(job_opening=job_opening,
                                                     job_seeker=job_seeker)
            application.delete()

            messages.success(request, 'Application deleted successfully!')
        else:
            messages.warning(request, 'You have not applied for this job.')

    except Exception as e:
        messages.error(request, f'Error deleting application: {str(e)}')

    return redirect('careers:my_applications')


@login_required
def view_job_seeker(request):
    if not hasattr(request.user, 'recruiter'):
        return redirect('careers:homepage')

    query = request.GET.get('q', '')
    min_experience = request.GET.get('min_experience', '')
    max_experience = request.GET.get('max_experience', '')
    expertise = request.GET.get('expertise', '')

    job_seekers = JobSeeker.objects.all()
    all_expertise = Expertise.objects.all()

    if query:
        job_seekers = job_seekers.filter(
            Q(user_ptr__first_name__icontains=query) | Q(
                user_ptr__last_name__icontains=query)
        )

    if min_experience:
        job_seekers = job_seekers.filter(work_experience__gte=min_experience)

    if max_experience:
        job_seekers = job_seekers.filter(work_experience__lte=max_experience)

    if expertise:
        job_seekers = job_seekers.filter(
            competence__expertise__skill=expertise)

    context = {
        'job_seekers': job_seekers,
        'query': query,
        'min_experience': min_experience,
        'max_experience': max_experience,
        'expertise': expertise,
        'all_expertise': all_expertise
    }

    return render(request, 'careers/view_job_seeker.html', context)


@method_decorator(login_required, name='dispatch')
class MyApplicationView(View):
    template_name = 'careers/my_applications.html'

    def get(self, request, *args, **kwargs):
        job_seeker = request.user.jobseeker

        applications = JobApplication.objects.filter(job_seeker=job_seeker)

        context = {'applications': applications}
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class RecruiterJobApplicationView(View):
    template_name = 'careers/recruiter_job_applications.html'

    def get(self, request, *args, **kwargs):
        recruiter = request.user.recruiter

        job_openings = recruiter.jobopening_set.all()
        selected_job_opening = request.GET.get('job_opening')

        applications = JobApplication.objects.filter(
            job_opening__recruiter=recruiter)

        applicant_name = request.GET.get('applicant_name')
        if applicant_name:
            applications &= JobApplication.objects.filter(
                Q(job_seeker_id__user_ptr__first_name__icontains=applicant_name) | Q(
                    job_seeker_id__user_ptr__last_name__icontains=applicant_name)
            )

        if selected_job_opening:
            applications = applications.filter(
                job_opening_id=selected_job_opening)

        context = {
            'applications': applications,
            'applicant_name': applicant_name,
            'job_openings': job_openings,
            'selected_job_opening': selected_job_opening,
        }
        return render(request, self.template_name, context)


@login_required
def update_recruiter(request, recruiter_id, company_id):
    recruiter = get_object_or_404(Recruiter, recruiter_id=recruiter_id)

    if request.method == 'POST':
        form = RecruiterUpdateForm(request.POST, instance=recruiter)
        if form.is_valid():
            form.save()
            return redirect('careers:recruiter_management',
                            company_id=company_id)
    else:
        form = RecruiterUpdateForm(instance=recruiter)

    return render(request, 'careers/update_recruiter.html',
                  {'form': form, 'recruiter': recruiter})


@login_required
def delete_recruiter(request, recruiter_id, company_id):
    recruiter = get_object_or_404(Recruiter, recruiter_id=recruiter_id)

    if request.method == 'POST':
        recruiter.delete()
        return redirect('careers:recruiter_management', company_id=company_id)

    return render(request, 'careers/delete_recruiter.html',
                  {'recruiter': recruiter})
