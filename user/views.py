from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def DashboardView(request):
    return render(request, 'user/dashboard.html')
    # if request.user.is_authenticated:
    #     return render(request, 'dashboard.html')
    # else:
    #     return render(request, 'createonlineexam/login.html')

