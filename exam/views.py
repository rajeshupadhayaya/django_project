from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse
import exam.functions, json, django.db
from .models import Question, Answers, ExamCreateDetails, Account, Student_Exams, Exam_Result
from django.core.mail import send_mail
from django.views.generic import View
import datetime
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView
from django.shortcuts import redirect
from django.core import serializers
from .serializers import AccountSerializer

# Create your views here.
# def index(request):
#     return render(request, 'createonlineexam/index.html')
num_range = 2

class IndexView(generic.TemplateView):

    template_name = 'createonlineexam/index.html'


class Objective_exam_View(generic.TemplateView):
    # context_object_name = 'question_list'
    template_name = 'createonlineexam/objective_exam.html'

# class Objective_exam_create_View(generic.):
#     list = {'n' : range(10)}
#     context_object_name = 'list'
#     template_name = 'createonlineexam/objective_create.html'


def Objective_exam_create_View(request):
    # loop['loop_times'] = range(1, 8)
    return render(request, 'createonlineexam/objective_create.html',context={'loop_times': range(1, num_range+1)})

def Objective_exam_submited_sucess_View(request):
    # loop['loop_times'] = range(1, 8)
    return render(request, 'createonlineexam/objective_create.html',context={'loop_times': range(1, num_range+1)})


@transaction.atomic
def Objective_exam_submit_View(request):

    if request.method == 'POST':
        exam_id = datetime.datetime.now().strftime("EX%y%m%d%H%M%S%f")
        username = request.POST['name']
        emailid = request.POST['mailid']
        examName = request.POST['examname']
        contact_no = int(request.POST['phonenumber'])
        examDuration = '00:20'
        exam_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # with transaction:
        examDetail_set = ExamCreateDetails(username=username, email_id = emailid,exam_create_date=exam_creation_time, exam_id = exam_id,
                                             exam_duration=examDuration,contact_no=contact_no,exam_name=examName)
        # try:
        examDetail_set.save()
        for i in range(1,num_range+1):
            ques = request.POST['ques'+str(i)].strip()
            ansa = request.POST['ans'+str(i) + 'a'].strip()
            ansb = request.POST['ans'+str(i) + 'b'].strip()
            ansc = request.POST['ans'+str(i) + 'c'].strip()
            ansd = request.POST['ans'+str(i) + 'd'].strip()
            ansCorrect = request.POST['ans'+str(i) + 'correct'].strip()
            question_set = Question(question_number=i, question_text=ques, exam_id_id = exam_id,
                                    exam_create_date=exam_creation_time)
            answer_set = Answers(question_number=i, choice_1=ansa, choice_2= ansb, choice_3=ansc, choice_4=ansd,
                                 correct_choice=ansCorrect, exam_id_id=exam_id)
            # if(question_set.save() & answer_set.save() & examDetail_set.save()):
            #     return HttpResponseRedirect(reverse('createonlineexam:submit_success', args=(exam_id,)))
            question_set.save()
            answer_set.save()
        return render(request, 'createonlineexam/exam_create_success.html', context={'exam_id': exam_id})

        #
        # except (Exception):
        #     # print(Exception)
        #     return render(request, 'createonlineexam/error.html')


class Result_View(View):

    template_name = 'createonlineexam/result_display.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        exam_id = request.POST['exam_id']
        results = Exam_Result.objects.filter(exam_id=exam_id)
        return render(request, self.template_name, context={'results': results, 'exam_id': exam_id})


class Exam_View(generic.ListView):
    template_name = 'createonlineexam/student_exam.html'
    context_object_name = 'questions'
    exam_id = ''

    def get_queryset(self):
        self.exam_id = self.kwargs['exam_id']
        question_set = []
        questions = Question.objects.filter(exam_id_id=self.exam_id)

        for ques in questions:
            answers = Answers.objects.filter(question_number=ques.question_number, exam_id=self.exam_id)
            question_set.append({'ques': ques, 'ans': serializers.serialize("python", answers)})

        if question_set:
            return [self.exam_id, question_set]
        else:
            raise Http404("Exam does not exist")


class Student_Result(generic.ListView):
    template_name = 'createonlineexam/exam_result.html'
    context_object_name = 'result'

    def get_queryset(self):
        id = self.kwargs['id']
        return Exam_Result.objects.get(pk=id)

    # def get(self, request, *args, **kwargs):
    #     name = kwargs['student_name']
    #     result = kwargs['result']
    #     return render(request, 'createonlineexam/exam_result.html', context={'name': name, 'result': result})


class Student_Exam_submit(View):

    def post(self, request):
        marks = 0
        email = request.POST['student_email'].strip()
        name = request.POST['student_name'].strip()
        phone_no = request.POST['student_phone_no'].strip()
        exam_id = request.POST['exam_id'].strip()
        exam_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        for i in range(1, num_range+1):
            correct_ans = Answers.objects.filter(question_number=i, exam_id=exam_id)[0]
            ans = request.POST['ans'+str(i)]
            exam_sheet = Student_Exams(name=name, email_id=email, phone_no=phone_no,
                                               question_number=i,exam_date=exam_creation_time,
                                               answer=ans, exam_id=correct_ans.exam_id)
            exam_sheet.save()
            if ans == correct_ans.correct_choice:
                marks +=1

        result = ((marks/num_range) * 100)

        exam_detail = ExamCreateDetails.objects.get(exam_id=exam_id)

        score = Exam_Result(name=name, email_id=email, phone_no=phone_no, exam_date=exam_creation_time,
                         score=result, exam_id=exam_detail)
        score.save()

        return redirect('onlineexam:student_result', id=score.pk)


class Search_View(generic.ListView):
    # model= Exam_create_details
    template_name = 'createonlineexam/search_result.html'
    context_object_name = 'search_result'
    # def get(self,request,*args, **kwargs):
    #     print ('hello')

    def get_queryset(self):
        examName = self.request.GET.get('search_parm')

        try:
            # self.question = Question.objects.filter(question_text__icontains=examName) ##icontains for case-insensitive query
            self.question = Question.objects.filter(
                    Q(question_text__icontains=examName) | Q(question_text__istartswith=examName)
            ).select_related('exam_id') ##icontains for case-insensitive query
            # print(self.question)

            # return (self.question)
            # print(self.question)
            return exam.functions.search_result_view(self.question)

        except Question.DoesNotExist:
            return 'No result found'


def login_auth(request):
    username = request.POST.get('logInEmail')
    password = request.POST.get('logInPassword')
    print(username, password)
    user = auth.authenticate(username = username, password = password)
    print(user)
    if user is not None:
        auth.login(request, user)
        return redirect('onlineexam:dashboard')
    else:

        return render(request,'createonlineexam/login.html')

def register_user(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.POST)
        # first_name = request.POST.get('registerName')
        # email = request.POST.get('registerEmail')
        # password = request.POST.get('registerPassword')
        # conf_password = request.POST.get('registerPassword1')
        # if conf_password!=password:
        #     return HttpResponse('Confirm Password did not matched with password')
        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)
            auth.login(request, account)
            return redirect('onlineexam:dashboard')
        else:
            print(serializer.errors)
    else:
        raise Http404("Page not found")


def forget_password(request):
    return HttpResponse('password generated')


def search_exam_ajax(request):
    output_to_front = ''
    if request.method == 'POST':
        search_parm = request.POST['examName'].strip()
        try:
            # search_result = Question.objects.get(question_text=search_parm)
            search_result = Question.objects.filter(question_text__contains=search_parm).values_list('question_text',flat=True).distinct()[:5]
            for question_text in search_result:
            # output_to_front = """
            # <a href="createonlineexam/search?search_parm='""" + ques + """'" ><li class="search-list list-group-item">'"""+ ques + """'</li></a>'
            # """
                output_to_front += '<a href = "/search?search_parm=' + str(question_text) + '"><li class="search-list list-group-item">' + str(question_text) + '</li></a>'
            return HttpResponse(output_to_front)
        except Question.DoesNotExist:
            return HttpResponse('No exam found')


def Send_email(request):
    response_data = {}
    response_data['result'] = ''
    response_data['message'] = ''

    if request.method == 'POST':

        requester_mail = request.POST['email'].strip()
        requester_name = request.POST['name'].strip()
        requester_msg = request.POST['message'].strip()
        receiver = 'rajeshupadhayaya@gmail.com'
        subject = 'Suggestion Send by Mr/Ms. ' + requester_name


        if requester_mail == '' or requester_name == '' or requester_msg =='':
            # return HttpResponse('Please provide inputs!!!')
            response_data['result'] = 'fail'
            response_data['message'] = 'Please provide inputs!!!'

        else:

            if exam.functions.sendMail(subject,requester_msg, requester_mail, receiver,requester_name):
               # return HttpResponse('Thank you for Contacting us')
               response_data['result'] = 'sucess'
               response_data['message'] = 'Thank you for Contacting us'
            else:
                response_data['result'] = 'fail'
                response_data['message'] = 'Oops!!! Something went wrong, Please try again....'
                # return HttpResponse('Oops!!! Something went wrong, Please try again....')

    else:
        response_data['result'] = 'fail'
        response_data['message'] = 'invalid request'
        # return HttpResponse('invalid request')
    return HttpResponse(json.dumps(response_data), content_type='application/json')