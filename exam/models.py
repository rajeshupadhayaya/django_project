from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class ExamCreateDetails(models.Model):
    username = models.CharField(max_length=200)
    email_id = models.CharField(max_length=100)
    exam_id = models.CharField(max_length=20,unique=True)
    exam_create_date=models.DateTimeField(auto_now_add=False)
    exam_name = models.CharField(max_length=100,default='Exam')
    exam_duration = models.CharField(max_length=5)
    exam_password = models.CharField(max_length=200,default=0)
    contact_no = models.CharField(max_length=12, default=0)
    country_code = models.CharField(max_length=5,default=0)

    # def __str__(self):              # __unicode__ on Python 2
    #     return self.exam_id

    class Meta:
        indexes = [
            models.Index(fields=['username', 'email_id']),
            models.Index(fields=['username'], name='user_name_idx'),
        ]


class Question(models.Model):
    question_number = models.IntegerField()
    question_text = models.CharField(max_length=200)
    exam_id = models.ForeignKey(ExamCreateDetails, to_field='exam_id',on_delete=models.CASCADE)
    exam_create_date = models.DateTimeField(auto_now_add=False)
    # exam_duration = models.DateTimeField(auto_now_add=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.question_text


class Student_Exams(models.Model):
    name = models.CharField(max_length=100)
    email_id = models.EmailField()
    phone_no = models.CharField(max_length=20)
    question_number = models.IntegerField()
    answer = models.CharField(max_length=200)
    exam_id = models.ForeignKey(ExamCreateDetails, to_field='exam_id',on_delete=models.CASCADE)
    exam_date = models.DateTimeField(auto_now_add=False)
    # exam_duration = models.DateTimeField(auto_now_add=False)
    # def __str__(self):              # __unicode__ on Python 2
    #     return self.question_text


class Exam_Result(models.Model):
    name = models.CharField(max_length=100)
    email_id = models.EmailField()
    phone_no = models.CharField(max_length=20)
    exam_id = models.ForeignKey(ExamCreateDetails, to_field='exam_id',on_delete=models.CASCADE)
    exam_date = models.DateTimeField(auto_now_add=False)
    score = models.DecimalField(max_digits=5, decimal_places=2)


class Answers(models.Model):
    question_number = models.IntegerField()
    exam_id = models.ForeignKey(ExamCreateDetails, to_field='exam_id',on_delete=models.CASCADE)
    choice_1 = models.CharField(max_length=50)
    choice_2 = models.CharField(max_length=50)
    choice_3 = models.CharField(max_length=50)
    choice_4 = models.CharField(max_length=50)
    correct_choice = models.CharField(max_length=50)

    # def __str__(self):              # __unicode__ on Python 2
    #
    #     return self.correct_choice
    class Meta:
        unique_together = [['exam_id', 'question_number']]


class AccountManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        # if not kwargs.get('username'):
        #     raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email),
            user_type=kwargs.get('user_type'), first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            profile_pic='emp.png'
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account



class Account(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        (1, 'teacher'),
        (2, 'student')
    )
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_pic = models.CharField(max_length=50, blank=True)
    # tagline = models.CharField(max_length=140, blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'first_name']
    full_name = [first_name, last_name]

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join(self.full_name)

    def get_short_name(self):
        return self.first_name

    def get_user_type(self):
        return self.user_type

