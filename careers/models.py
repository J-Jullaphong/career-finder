from django.contrib.auth.models import User
from django.db import models


class JobSeeker(User):
    job_seeker_id = models.CharField(max_length=8, primary_key=True)
    work_experience = models.DecimalField(max_digits=2, decimal_places=1)
    phone_number = models.CharField(max_length=10, help_text="Contact number")

    def save(self, *args, **kwargs):
        if not self.job_seeker_id:
            last_job_seeker = JobSeeker.objects.order_by(
                'job_seeker_id').last()
            if last_job_seeker:
                last_id = int(last_job_seeker.job_seeker_id[2:])
                new_id = f'JS{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'JS000001'
            self.job_seeker_id = new_id
        super(JobSeeker, self).save(*args, **kwargs)


class Expertise(models.Model):
    expertise_id = models.CharField(max_length=8, primary_key=True)
    skill = models.CharField(max_length=50, help_text="Job seeker's skill")

    def save(self, *args, **kwargs):
        if not self.expertise_id:
            last_expertise = Expertise.objects.order_by('expertise_id').last()
            if last_expertise:
                last_id = int(last_expertise.expertise_id[2:])
                new_id = f'EX{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'EX000001'
            self.expertise_id = new_id
        super(Expertise, self).save(*args, **kwargs)

    def __str__(self):
        return self.skill


class Competence(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    expertise = models.ForeignKey(Expertise, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('job_seeker', 'expertise'),)


class Recruiter(User):
    recruiter_id = models.CharField(max_length=8, primary_key=True)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.recruiter_id:
            last_recruiter = Recruiter.objects.order_by('recruiter_id').last()
            if last_recruiter:
                last_id = int(last_recruiter.recruiter_id[2:])
                new_id = f'RE{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'RE000001'
            self.recruiter_id = new_id
        super(Recruiter, self).save(*args, **kwargs)


class Company(User):
    company_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10, help_text="Contact number")
    street = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=5, help_text="Postal code")

    def save(self, *args, **kwargs):
        if not self.company_id:
            last_company = Company.objects.order_by('company_id').last()
            if last_company:
                last_id = int(last_company.company_id[2:])
                new_id = f'CO{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'CO000001'
            self.company_id = new_id
        super(Company, self).save(*args, **kwargs)


class JobOpening(models.Model):
    job_opening_id = models.CharField(max_length=8, primary_key=True)
    job_title = models.CharField(max_length=30)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    job_function = models.ForeignKey('JobFunction', on_delete=models.CASCADE)
    job_type = models.ForeignKey('JobType', on_delete=models.CASCADE)
    required_work_experience = models.DecimalField(max_digits=2,
                                                   decimal_places=1)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.job_opening_id:
            last_job_opening = JobOpening.objects.order_by(
                'job_opening_id').last()
            if last_job_opening:
                last_id = int(last_job_opening.job_opening_id[2:])
                new_id = f'JO{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'JO000001'
            self.job_opening_id = new_id
        super(JobOpening, self).save(*args, **kwargs)


class Requirement(models.Model):
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE)
    expertise = models.ForeignKey(Expertise, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('job_opening', 'expertise'),)


class JobApplication(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('job_seeker', 'job_opening'),)


class JobFunction(models.Model):
    job_function_id = models.CharField(max_length=8, primary_key=True)
    function = models.CharField(max_length=30,
                                help_text="Job function description")

    def save(self, *args, **kwargs):
        if not self.job_function_id:
            last_job_function = JobFunction.objects.order_by(
                'job_function_id').last()
            if last_job_function:
                last_id = int(last_job_function.job_function_id[2:])
                new_id = f'JF{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'JF000001'
            self.job_function_id = new_id
        super(JobFunction, self).save(*args, **kwargs)

    def __str__(self):
        return self.function


class JobType(models.Model):
    job_type_id = models.CharField(max_length=8, primary_key=True)
    type = models.CharField(max_length=30, help_text="Type of job")

    def save(self, *args, **kwargs):
        if not self.job_type_id:
            last_job_type = JobType.objects.order_by('job_type_id').last()
            if last_job_type:
                last_id = int(last_job_type.job_type_id[2:])
                new_id = f'JT{str(last_id + 1).zfill(6)}'
            else:
                new_id = 'JT000001'
            self.job_type_id = new_id
        super(JobType, self).save(*args, **kwargs)

    def __str__(self):
        return self.type
