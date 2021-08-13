from django.shortcuts import render, redirect
from.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta
from django.contrib.auth import login as auth_login
from django.db.models import Q
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    return render(request,'index.html')

def job(request):
    data1 = Job.objects.filter(paid="PAID100")
    data2 = Job.objects.filter(paid="PAID50")
    data = Job.objects.all().order_by('-creationdate')
    d={'data': data,'data1': data1,'data2': data2 }
    return render(request,'job.html',d)

def search(request):
    if request.method == 'GET':
        search= request.GET['search']
        filtertitle=Job.objects.filter(title__icontains=search)
        filtercompany = Job.objects.filter(company__icontains=search)
        filter= filtertitle.union(filtercompany).order_by('-creationdate')
    d = {'filter': filter,'search': search}
    return render(request, 'search.html', d)

def search1(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    if request.method == 'GET':
        search= request.GET['search']
        filtertitle=Job.objects.filter(title__icontains=search)
        filtercompany = Job.objects.filter(company__icontains=search)
        data= filtertitle.union(filtercompany).order_by('-creationdate')
    d = {'data': data,'search': search,'student': student}
    return render(request, 'search1.html', d)

def search2(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    if request.method == 'GET':
        search= request.GET['search']
        filtertitle   = Job.objects.filter(title__icontains=search)
        filtercompany = Job.objects.filter(company__icontains=search)
        data= filtertitle.union(filtercompany).order_by('-creationdate')
    d = {'data': data,'search': search,'recruiter': recruiter}
    return render(request, 'search2.html', d)

def videosearch(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    if request.method == 'GET':
        search= request.GET['search']
        captionfilter   = Video.objects.filter(caption__icontains=search)
        typefilter      = Video.objects.filter(type__icontains=search)
        caption = captionfilter.union(typefilter)
    d = {'caption': caption,'search': search,}
    return render(request, 'videosearch.html', d)

def vacancysearch(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    caption  = Video.objects.filter(type__icontains="Vacancy")
    d = {'caption': caption}
    return render(request, 'vacancysearch.html', d)

def resumesearch(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    caption  = Video.objects.filter(type__icontains="Resume")
    d = {'caption': caption}
    return render(request, 'resumesearch.html', d)

def todaysearch(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    caption  = Video.objects.filter(creationdate=date.today())
    d = {'caption': caption}
    return render(request, 'todaysearch.html', d)

def yesterdaysearch(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    yesterday = date.today() - timedelta(days=1)
    caption  = Video.objects.filter(creationdate=yesterday)
    d = {'caption': caption}
    return render(request, 'yesterdaysearch.html', d)


def myvideo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    myvideo = Video.objects.filter(user=user)
    d = {'myvideo': myvideo}
    return render(request, 'myvideo.html', d)

def latestjob(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Job.objects.all().order_by('-creationdate')
    data1 = Job.objects.filter(paid="PAID100")
    data2 = Job.objects.filter(paid="PAID50")
    d={'data': data,'student':student,'data1':data1,'data2':data2}
    return render(request, 'latestjob.html',d)

def latestjobpageforrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    data = Job.objects.all().order_by('-creationdate')
    data1 = Job.objects.filter(paid="PAID100")
    data2 = Job.objects.filter(paid="PAID50")
    d={'data': data,'recruiter':recruiter,'data1':data1,'data2':data2 }
    return render(request, 'latestjobpageforrecruiter.html',d)

def delete_user(request,pid):
    student = StudentUser.objects.get(id=pid)
    student.delete()
    return redirect(userdata)

def delete_recruiter(request,pid):
    recruiter = Recruiter.objects.get(id=pid)
    recruiter.delete()
    return redirect(recruiterdata)

def delete_post(request,pid):
    post = Job.objects.get(id=pid)
    post.delete()
    return redirect(recruitermainpage)

def delete_postbyadmin(request,pid):
    post = Job.objects.get(id=pid)
    post.delete()
    return redirect(postofeveryrecruiter)

def delete_resume(request):
    user = request.user
    student = StudentUser.objects.get(user=user)
    student.resume.delete()
    return redirect(userprofileupdate)

def delete_apply(request,pid):
    apply = Apply.objects.get(id=pid)
    apply.delete()
    return redirect(userstatusbar)

def recruitermainpage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    data=Job.objects.filter(recruiter=recruiter)
    d={'data': data,'recruiter':recruiter}
    return render(request,'recruitermainpage.html',d)

def postofeveryrecruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    recruiter = Recruiter.objects.get(id=pid)
    data = Job.objects.filter(recruiter=recruiter)
    d = {'data': data }
    return render(request, 'postofeveryrecruiter.html', d)


def bosspage(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    data1 = Job.objects.filter(paid="PAID100")
    data2 = Job.objects.filter(paid="PAID50")
    data = Job.objects.all().order_by('-creationdate')
    d = {'data1': data1, 'data2': data2,'data': data,}
    return render(request,'bosspage.html',d)

def login(request):
    # ACCEPT DATA FROM FORM START
    error=""
    if request.method == "POST":
       e = request.POST['email']
       p = request.POST['pswd']
       user = authenticate(request, username=e, password=p)
       if user:
           try:
               user1 = StudentUser.objects.get(user=user)
               if user1.type == "Student":
                   auth_login(request, user)
                   error = "no"
               else:
                   error = "yes"
           except:
               error = "yes"
       else:
           error="yes"
    d = {'error': error}
    return render(request,'login.html',d)

def recruiterlogin(request):
    # ACCEPT DATA FROM FORM START
    error=""
    if request.method == "POST":
       e = request.POST['email']
       p = request.POST['pswd']
       user = authenticate(request, username=e, password=p)
       if user:
           try:
               user1 = Recruiter.objects.get(user=user)
               if user1.type == "Recruiter":
                   auth_login(request, user)
                   error = "no"
               else:
                   error = "yes"
           except:
               error = "yes"
       else:
           error="yes"
    d = {'error': error}
    return render(request,'recruiterlogin.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method == 'POST':
        cp = request.POST['currentpassword']
        np = request.POST['newpassword']
        try:
             matched=User.objects.get(id=request.user.id)
             if matched.check_password(cp):
                 matched.set_password(np)
                 matched.save()
                 error="no"
             else:
                 error="not"
        except:
            error="yes"
    d={'error':error}

    return render(request, 'changepassword.html',d)

def changepasswordforrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    error = ""
    if request.method == 'POST':
        cp = request.POST['currentpassword']
        np = request.POST['newpassword']
        try:
             matched=User.objects.get(id=request.user.id)
             if matched.check_password(cp):
                 matched.set_password(np)
                 matched.save()
                 error="no"
             else:
                 error="not"
        except:
            error="yes"
    d={'error':error}

    return render(request, 'changepasswordforrecruiter.html',d)

def usersignup(request):
    # ACCEPT DATA FROM FORM START
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        g = request.POST['gender']
        image= request.FILES['image']
        e = request.POST['email']
        p = request.POST['pswd']
        if User.objects.filter(username=e).exists():
            error = "yes"
        else:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, email=e, password=p, )
            StudentUser.objects.create(user=user, mobile=con, image=image, gender=g, type="Student")
            error = "no"

    d = {'error': error}

    # ACCEPT DATA FROM FORM END
    return render(request,'usersignup.html',d)

def recruitersignup(request):
    # ACCEPT DATA FROM FORM START
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        g = request.POST['gender']
        c = request.POST['company']
        img = request.FILES['image']
        e = request.POST['email']
        p = request.POST['pswd']
        if User.objects.filter(username=e).exists():
            error = "yes"
        else:
            user = User.objects.create_user(first_name=f, last_name=l,email=e, username=e, password=p,)
            Recruiter.objects.create(user=user, mobile=con, gender=g, company=c, image=img, type="Recruiter", status="pending")
            error = "no"

    d = {'error': error}

    # ACCEPT DATA FROM FORM END
    return render(request,'recruitersignup.html',d)

def adminlogin(request):
    error = ""
    if request.method == 'POST':
        e = request.POST['email']
        p = request.POST['pswd']
        user = authenticate(username=e, password=p)
        try:
           if user.is_staff:
              auth_login(request, user)
              error="no"
           else:
              error = "yes"
        except:
              error = "yes"
    d = {'error': error}

    return render(request,'adminlogin.html',d)

def userdata(request):
    data = StudentUser.objects.all
    d={'data': data}
    return render(request, 'userdata.html',d)

def recruiterdata(request):
    data = Recruiter.objects.all
    d={'data': data}
    return render(request, 'recruiterdata.html',d)

def addjob(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    # ACCEPT DATA FROM FORM START
    error = ""
    if request.method == 'POST':
        st = request.POST['startdate']
        en = request.POST['enddate']
        jo = request.POST['jobtitle']
        de = request.POST['description']
        ex = request.POST['experience']
        sa= request.POST['salary']
        pe = request.POST['permonth']
        sk = request.POST['skill']
        co = request.POST['company']
        lo = request.POST['location']
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
           Job.objects.create(recruiter=recruiter,start_date=st, end_date=en, salary=sa, permonth=pe, title=jo, description=de, experience=ex, location=lo, skill=sk, company=co, creationdate=date.today())
           error = "no"
        except:
           error = "yes"
    d = {'error': error}

    # ACCEPT DATA FROM FORM END
    return render(request, 'addjob.html',d)

def updatepost(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    # ACCEPT DATA FROM FORM START
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        st = request.POST['startdate']
        en = request.POST['enddate']
        jo = request.POST['jobtitle']
        de = request.POST['description']
        ex = request.POST['experience']
        sa= request.POST['salary']
        pe = request.POST['permonth']
        sk = request.POST['skill']
        co = request.POST['company']
        lo = request.POST['location']

        job.title = jo
        job.description = de
        job.experience = ex
        job.salary = sa
        job.permonth = pe
        job.skill = sk
        job.company = co
        job.location = lo
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if st:
            try:
                job.start_date = st
                job.save()
            except:
                pass
        else:
            pass

        if en:
            try:
                job.end_date = en
                job.save()
            except:
                pass
        else:
            pass
    d = {'error': error, 'job': job}

    # ACCEPT DATA FROM FORM END
    return render(request, 'updatepost.html',d)

def userprofileupdate(request):
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']
        n = request.POST['n']


        student.user.first_name = fn
        student.user.last_name = ln
        student.user.username = e
        student.mobile = n

        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"
        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error = "no"
        except:
            error = "yes"
        try:
            g = request.POST['g']
            student.gender = g
            student.save()
            error="no"
        except:
            error = "yes"
    d = {'student': student, 'error': error}
    return render(request, 'userprofileupdate.html',d)

def recruiterprofileupdate(request):
    user=request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']
        c = request.POST['c']
        n = request.POST['n']

        recruiter.user.first_name = fn
        recruiter.user.last_name  = ln
        recruiter.user.username = e
        recruiter.mobile = n
        recruiter.company = c
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes"
        try:
            i = request.FILES['image']
            recruiter.image= i
            recruiter.save()
            error="no"
        except:
            error="yes"

    d={'recruiter': recruiter,'error':error}
    return render(request, 'recruiterprofileupdate.html',d)

def detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data4 = Apply.objects.filter(student=student)

    li = []
    for i in data4:
        li.append(i.job.id)

    data5 = Job.objects.get(id=pid)
    resume= student.resume
    error = ""
    if request.method == 'POST':
        try:
            Apply.objects.create(job=data5, student=student, resume=resume, applied_date=date.today())
            error = "no"
        except:
            error = "yes"

    data3=Job.objects.get(id=pid)
    filter=Job.objects.filter(title__icontains=data3.title).order_by('-creationdate')
    d={'data3': data3,'li': li,'error': error,'student': student,'filter': filter}
    return render(request,'detail.html',d)

def detailforrecruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Job.objects.get(id=pid)
    d={'data': data}
    return render(request, 'detailforrecruiter.html',d)

def userstatusbar(request):
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    d = {'data': data}
    return render(request,'userstatusbar.html',d)

def singlestatus(request,pid):
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student=student)
    data1 = Apply.objects.filter(id=pid)
    for n in data1:
        statue=n.status
    if statue:
        error = ""
        if statue == "Application Viewed":
            error = "Application Viewed"

        if statue == "Application Rejected":
            error = "Application Rejected"

        if statue == "Application Accepted":
            error = "Application Accepted"

        if statue == "Video Interview Scheduled":
            error = "Video Interview Scheduled"

        if statue == "Selected":
            error = "Selected"

        if statue == "Rejected":
            error = "Rejected"

        if statue == "Joining Letter":
            error = "Joining Letter"
    else:
        error = "none"
    d = {'data': data,'data1': data1,'error': error,}
    return render(request,'userstatusbar.html',d)

def statuschange(request,pid):
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    data = Apply.objects.filter(job__in=job)
    data1 = Apply.objects.filter(id=pid)
    for n in data1:
        statue=n.status

    if statue:
        error = ""
        if statue == "Application Viewed":
            error = "Application Viewed"

        if statue == "Application Rejected":
            error = "Application Rejected"

        if statue == "Application Accepted":
            error = "Application Accepted"

        if statue == "Video Interview Scheduled":
            error = "Video Interview Scheduled"

        if statue == "Selected":
            error = "Selected"

        if statue == "Rejected":
            error = "Rejected"

        if statue == "Joining Letter":
            error = "Joining Letter"
    else:
        error = "none"



    d = {'data':data, 'data1':data1,'error':error,}
    return render(request,'recruiterstatusbar.html',d)

def statusfieldkadata(request,pid):
    data1 = Apply.objects.filter(id=pid)
    for i in data1:
        i.status
        i.interviewdateaandtime
        i.joiningletter
    error = ""
    if request.method == 'POST':
        try:
            ac = request.POST['accept']
            i.status = ac
            i.save()
            error = "nahi"
        except:
           error = "hai"
        try:
            idtf = request.POST['interviewdatetimefield']
            i.interviewdateaandtime=idtf
            i.save()
            error = "nahi"
        except:
           error = "hai"
        try:
            jl = request.FILES['joiningletter']
            i.joiningletter = jl
            i.save()
            error = "nahi"
        except:
            error = "hai"
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    data = Apply.objects.filter(job__in=job)

    if i.status:
        error = ""
        if i.status == "Application Viewed":
            error = "Application Viewed"

        if i.status == "Application Rejected":
            error = "Application Rejected"

        if i.status == "Application Accepted":
            error = "Application Accepted"

        if i.status == "Video Interview Scheduled":
            error = "Video Interview Scheduled"

        if i.status == "Selected":
            error = "Selected"

        if i.status == "Rejected":
            error = "Rejected"

        if i.status == "Joining Letter":
            error = "Joining Letter"
    else:
        error = "none"



    d = {'error': error,'data': data,'data1': data1,}
    return render(request, 'recruiterstatusbar.html', d)

def recruiterstatusbar(request,):
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    data = Apply.objects.filter(job__in=job)
    d = {'data':data,}
    return render(request,'recruiterstatusbar.html',d)

def countofappliedstudent(request):
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d = {'job':job}
    return render(request,'countofappliedstudent.html',d)

def video(request):
    error=''

    if request.method == 'POST':
        v = request.FILES['videoo']
        c = request.POST['caption']
        t = request.FILES['image']
        ty = request.POST['type']


        try:
            Video.objects.create(video=v, caption=c, thumbnail=t,type=ty,creationdate=date.today(),user=request.user)
            error = "yes"
        except:
            error = "no"
    user = request.user
    if user:
        try:
            user1 = Recruiter.objects.get(user=user)
            if user1.type == "Recruiter":
                error = "candidate1"

        except:
            user1 = StudentUser.objects.get(user=user)
            if user1.type == "Student":
                error = "candidate2"

    video=Video.objects.all()
    d={'video': video,'error': error,'user': user}
    return render(request,'video.html',d)

def addresume(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':

        try:
           add = request.FILES['addresume']
           student.resume = add
           student.save()
           error = "nahi"
        except:
           error = "hai"

    d = {'error': error, 'student': student}
    return render(request, 'userprofileupdate.html',d)

def aboutus(request):
    return render(request, 'aboutus.html')

def placedstudent(request):
    return render(request, 'placedstudent.html')

def interviewquestion(request):
    return render(request, 'interviewquestion.html')

def feedback(request):
    error = ""
    if request.method == "POST":
        question = request.POST['question']
        answer = request.POST['answer']
        try:
            Feedback.objects.create(title=question, content=answer,date=date.today() )
            error = "no"
        except:
            error = "yes"

    material = Feedback.objects.all().order_by('-date')
    d = {'error': error, 'material': material, }
    return render(request, 'feedback.html', d)

def deletefeedback(request,pid):
    apply = Feedback.objects.get(id=pid)
    apply.delete()
    return redirect(feedback)

def bestyoutubechannel(request):
    return render(request, 'interviewquestion.html')

def grandmaa(request):
    return render(request, 'grandmaa.html')