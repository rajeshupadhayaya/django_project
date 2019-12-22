import smtplib
from django.core.mail import send_mail
from .models import Question,Answers,ExamCreateDetails
from django.core import serializers
import json

def sendMail(subject,requester_msg, requester_mail, receiver,requester_name):

    subject = 'Suggestion Send by Mr/Ms. ' + requester_name
    try:
        send_mail(subject, requester_msg, requester_mail,[receiver], fail_silently=False)
        return True

    except smtplib.SMTPException:
        return False

def search_result_view(question):
    template_view = ''
    data = json.loads(serializers.serialize("json", question))

    for ques in data:
        examname = ExamCreateDetails.objects.get(exam_id=ques['fields']['exam_id'])
        template_view += '<a href="#">'+ examname.exam_name +' </a><div class="search-desc">'+ \
                         ques['fields']['question_text'] + '</div>'
    return template_view