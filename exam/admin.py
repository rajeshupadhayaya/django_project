from django.contrib import admin

# Register your models here.
from .models import ExamCreateDetails
from .models import Question
from .models import Answers
from .models import Account


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_number','question_text','exam_id', 'exam_create_date']


admin.site.register(ExamCreateDetails)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answers)
admin.site.register(Account)