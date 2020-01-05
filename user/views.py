from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views import View
from django.core.files.storage import FileSystemStorage
import datetime
from django.shortcuts import redirect
from django.contrib import messages
from exam.models import Question, Answers, ExamCreateDetails, Account, Exam_Result
from django.db.models import Count
from exam.serializers import AccountSerializer
# Create your views here.

num_range = 2

@login_required
def DashboardView(request):
    examcreateddetails = ExamCreateDetails.objects.filter(email_id=request.user).count()
    examsubmitted = ExamCreateDetails.objects.filter(email_id=request.user).annotate(exam_submitted=Count('exam_result'))
    # print(examsubmitted[3].exam_submitted)
    return render(request, 'user/dashboard.html', context={'examcreateddetails':examcreateddetails})
    # if request.user.is_authenticated:
    #     return render(request, 'dashboard.html')
    # else:
    #     return render(request, 'createonlineexam/login.html')


class ProfileView(View):

    template_name = 'user/profile.html'

    def get(self,request):

        return render(request, self.template_name)

    def post(self,request):

        user = Account.objects.get(pk=request.user.id)

        try:
            profile_pic = request.FILES['photo']
        except:
            profile_pic = False
        # user = Account.objects.get(pk=request.user.id)
        # print(user)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']

        if profile_pic:
            ext = profile_pic.name.split(".")[1].lower()
            img_name = 'IMG' + str(int(datetime.datetime.now().timestamp()))+'.'+ext
            fs = FileSystemStorage()
            fs.save(img_name, profile_pic)
            user.profile_pic = img_name

        try:
            user.save()
            messages.success(request, 'Profile details updates successfully')
        except:
            messages.error(request, 'Error on updating data')

        return redirect('onlineexam:profile')


class AllExams(generic.ListView):
    template_name = 'user/all_exams.html'
    context_object_name = 'exams'

    def get_queryset(self):
        return ExamCreateDetails.objects.filter(email_id=self.request.user)


class CreateNewExam(generic.TemplateView):
    template_name = 'user/create_exam.html'

    def get_context_data(self, **kwargs):
        context = super(CreateNewExam, self).get_context_data(**kwargs)
        context['loop_times'] = range(1, num_range+1)
        return context

class SubmitCreateNewExam(View):

    def post(self,request):
        exam_id = datetime.datetime.now().strftime("EX%y%m%d%H%M%S%f")
        username = request.user.first_name
        emailid = request.user
        examName = request.POST['examname']
        contact_no = 0
        examDuration = '00:20'
        exam_creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # with transaction:
        examDetail_set = ExamCreateDetails(username=username, email_id=emailid, exam_create_date=exam_creation_time,
                                           exam_id=exam_id,
                                           exam_duration=examDuration, contact_no=contact_no, exam_name=examName)
        # try:
        examDetail_set.save()
        for i in range(1, num_range + 1):
            ques = request.POST['ques' + str(i)].strip()
            ansa = request.POST['ans' + str(i) + 'a'].strip()
            ansb = request.POST['ans' + str(i) + 'b'].strip()
            ansc = request.POST['ans' + str(i) + 'c'].strip()
            ansd = request.POST['ans' + str(i) + 'd'].strip()
            ansCorrect = request.POST['ans' + str(i) + 'correct'].strip()
            question_set = Question(question_number=i, question_text=ques, exam_id_id=exam_id,
                                    exam_create_date=exam_creation_time)
            answer_set = Answers(question_number=i, choice_1=ansa, choice_2=ansb, choice_3=ansc, choice_4=ansd,
                                 correct_choice=ansCorrect, exam_id_id=exam_id)
            # if(question_set.save() & answer_set.save() & examDetail_set.save()):
            #     return HttpResponseRedirect(reverse('createonlineexam:submit_success', args=(exam_id,)))
            question_set.save()
            answer_set.save()
        return render(request, 'user/exam_create_success.html', context={'exam_id': exam_id})

class Result_View(View):

    template_name = 'user/result_display.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        exam_id = request.POST['exam_id']
        results = Exam_Result.objects.filter(exam_id=exam_id)
        return render(request, self.template_name, context={'results': results, 'exam_id': exam_id})
