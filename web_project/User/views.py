from django.shortcuts import render, redirect, HttpResponse
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
# 장고 기본 유저 정보를 가져옴
from django.contrib.auth import get_user_model
from .models import HUser, Line, Worked, Profile, Eval
from .forms import SignupForm, SigninForm, ResendForm, ResetForm, LineForm, ProfForm
from django.utils import timezone

#이메일 인증
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import account_activation_token

#비밀번호
from django.contrib.auth.hashers import check_password

#회원가입 뷰
def signup(request):
    if request.method == "GET":
        return render(request, 'registration/signup.html', {'form':SignupForm()} )

    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.is_active = False
            user.save()
            hd = HUser(name=user.last_name+user.first_name, user=user)
            hd.save()
            pr = Profile(target=hd, )
            pr.save()
            current_site = get_current_site(request)
            # localhost:8000
            message = render_to_string('registration/user_active_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = "[성대한 과외] 회원가입 인증 메일입니다."
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return redirect(reverse("verification"))

        return render(request, "registration/signup.html", {"form": form})

#이메일에서 받은 인증메일을 눌렀을때 실행
def activate(request, uidb64, token):

    uid = force_text(urlsafe_base64_decode(uidb64))
    User = get_user_model()
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('signup_ok')
    else:
        return HttpResponse('비정상적인 접근입니다.')

# 비밀번호 재설정 인증 메일
def email_change_pw(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    User = get_user_model()
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "GET":
            return render(request, 'registration/reset.html', {'form':ResetForm()} )

        elif request.method == "POST":
            form = ResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('br', pg=1)

            return render(request, 'registration/reset.html', {'form':form()} )
    else:
        return HttpResponse('비정상적인 접근입니다.')


# 비밀번호 변경
def change_pw(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect('br', pg=1) #비밀번호가 성공적으로 변경되었다면 홈페이지로 리다이렉트
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, "registration/change_pw.html",context)

#로그인 뷰
def signin(request):#로그인 기능
    if request.method == "GET":
        return render(request, 'registration/signin.html', {'form':SigninForm()} )

    elif request.method == "POST":
        form = SigninForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        if form.is_valid():
            user = auth.authenticate(request, username=username, password=password)
            auth.login(request, user)

            return redirect('br', pg=1) #홈페이지로 이동

        return render(request, "registration/signin.html", {"form": form})
    else:
        form = SigninForm()
        return render(request, 'registration/signin.html',{'form':form})


# 회원가입 후 인증 뷰
def verification(request):
    return render(request, 'registration/verification.html', {})

def verification_resend(request):
    return render(request, 'registration/verification_resend.html', {})

# 회원가입 완료 뷰
def signup_ok(request):
    return render(request, 'registration/signup_ok.html', {})

# 이메일 재전송 및 전송 뷰
def resend(request):
    if request.method == "GET":
        return render(request, 'registration/resend.html', {'form':ResendForm()} )

    elif request.method == "POST":
        form = ResendForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user_email = form.cleaned_data['email']
            if User.objects.filter(email=user_email).exists():
                user = User.objects.get(email=user_email)
                current_site = get_current_site(request)
                # localhost:8000
                message = render_to_string('registration/resend_email.html',{
                    'user': user,
                    'domain': current_site.domain,
                    'site_name' : current_site.name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    'token': account_activation_token.make_token(user),
                })

                mail_subject = "[성대한 과외] 재전송 메일입니다."
                email = EmailMessage(mail_subject, message, to=[user_email])
                email.send()
            else:
                return HttpResponse('비정상적인 접근입니다.')

            return redirect(reverse("verification_resend"))

        return render(request, "registration/resend.html", {"form": form})
    else:
        form = ResendForm()
        return render(request, 'registration/resend.html',{'form':form})


@login_required
def user_prof(request, pk):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    targ = get_user_model().objects.all().filter(pk=pk)[0]
    prof = targ.handle.profile
    ev = targ.handle.rating.all()
    prof.score_update()
    return render(request, 'User/profile.html', {'prof': prof, 'user': user, 'eval': ev, 'targ': targ, 'talkable': talkable})


@login_required
def revise_prof(request, pk):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    prof = user.handle.profile
    if request.method == "POST":
        form = ProfForm(request.POST, instance=prof)
        if form.is_valid():
            p = form.save(commit=False)
            p.save()
            return redirect('profile', pk=pk)
    else:
        form = ProfForm(instance=prof)
    return render(request, 'User/revise_profile.html', {'form': form, 'user': user, 'talkable': talkable})

@login_required
def ask_to_talk(request, pk):
    user = request.user
    opn = get_user_model().objects.all().filter(pk=pk)[0]
    op = opn.my_post.all().filter(state='대기')
    if op:
        for myp in user.my_post.all().filter(state='대기'):
            myp.state = '대화중'
            myp.save()
        for yrp in op:
            yrp.state = '대화중'
            yrp.save()
        line = Line(content=user.handle.name + ': 대화가 시작되었습니다.', date=timezone.now(), alive=True)
        if user.handle.skku:
            line.teacher = user.handle
            line.student = opn.handle
        else:
            line.student = user.handle
            line.teacher = opn.handle
        line.save()
        return redirect('personal')
    else:
        return redirect('br', pg=1)    # 사이트 띄우고 누른 그 사이에 대화중인지 재확인하기 위함임.

@login_required
def personal(request):
    user = request.user.handle
    if user.skku:
        lines = Line.objects.all().filter(teacher=user, alive=True).order_by('date')
        if not lines:  # 1대1대화에 접근이 가능한 상태에서 상대가 결렬을 누른 경우.
            return redirect('br', pg=1)
        opn = Line.objects.all().filter(teacher=user, alive=True)[0].student
    else:
        lines = Line.objects.all().filter(student=user, alive=True).order_by('date')
        if not lines:  # 1대1대화에 접근이 가능한 상태에서 상대가 결렬을 누른 경우.
            return redirect('br', pg=1)
        opn = Line.objects.all().filter(student=user, alive=True)[0].teacher
    if user.skku:
        ar = user.line_t.all().filter(alive=True)
    else:
        ar = user.line_s.all().filter(alive=True)
    cons = False
    for a in ar:
        if a.content == user.name+'님 동의!':
            cons = True
    if request.method == "POST":
        if not lines:  # 1대1대화에 접근이 가능한 상태에서 상대가 결렬을 누른 경우.
            return redirect('br', pg=1)
        form = LineForm(request.POST)
        if form.is_valid():
            line = form.save(commit=False)
            line.content = user.name+': '+line.content
            line.writer_is_std = not user.skku
            line.date = timezone.now()
            line.alive = True
            if user.skku:
                line.teacher = user
                line.student = opn
            else:
                line.student = user
                line.teacher = opn
            line.save()
        return redirect('personal')
    else:
        if not lines:  # 1대1대화에 접근이 가능한 상태에서 상대가 결렬을 누른 경우.
            return redirect('br', pg=1)
        form = LineForm()
    return render(request, 'User/1to1.html', {'lines': lines, 'form': form, 'cons': cons})


def line_ref(request):
    user = request.user
    if user.handle.skku:
        lines = Line.objects.all().filter(teacher=user.handle, alive=True).order_by('date')
        opn = Line.objects.all().filter(teacher=user.handle, alive=True)[0].student
    else:
        lines = Line.objects.all().filter(student=user.handle, alive=True).order_by('date')
        opn = Line.objects.all().filter(student=user.handle, alive=True)[0].teacher
    lines.delete()
    op = opn.user.my_post.all().filter(state='대화중')
    for myp in user.my_post.all().filter(state='대화중'):
        myp.state = '대기'
        myp.save()
    for yrp in op:
        yrp.state = '대기'
        yrp.save()
    return redirect('br', pg=1)


def line_consent(request):
    user = request.user
    cons = Line(content=user.handle.name+'님 동의!', alive=True, date=timezone.now())
    if user.handle.skku:
        lines = Line.objects.all().filter(teacher=user.handle, alive=True).order_by('date')
        if not lines:  # 1대1대화에 접근이 가능한 상태에서 상대가 결렬을 누른 경우.
            return redirect('br', pg=1)
        opn = Line.objects.all().filter(teacher=user.handle, alive=True)[0].student
        cons.teacher = user.handle
        cons.student = opn
    else:
        lines = Line.objects.all().filter(student=user.handle, alive=True).order_by('date')
        if not lines:  # 1대1대화에 접근이 가능한 상태에서 상대가 결렬을 누른 경우.
            return redirect('br', pg=1)
        opn = Line.objects.all().filter(student=user.handle, alive=True)[0].teacher
        cons.student = user.handle
        cons.teacher = opn
    cons.save()
    if user.handle.skku:
        ar = opn.line_s.all().filter(alive=True)
    else:
        ar = opn.line_t.all().filter(alive=True)
    for a in ar:
        if a.content == opn.name+'님 동의!':
            for pst in user.my_post.all():
                pst.state = '완료'
                pst.save()
            for pst in opn.user.my_post.all():
                pst.state = '완료'
                pst.save()
            if user.handle.skku:
                w1 = Worked(teacher=user.handle, student=opn)
            else:
                w1 = Worked(teacher=opn, student=user.handle)
            wee = Worked.objects.all()
            for ww in wee:
                if ww == w1:
                    lines.delete()
                    return redirect('br', pg=1)
            w1.save()
            lines.delete()
            return redirect('br', pg=1)
    return redirect('personal')


def eval(request):
    user = request.user.handle
    talkable = True
    if user.skku:
        if user.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.line_s.all().filter(alive=True):
            talkable = False
    if request.method == "POST":
        target_name = request.POST.get('target', '')
        if target_name == '':
            return redirect('eval')
        targets = HUser.objects.all().filter(name=target_name)
        target = None
        for t in targets:
            if user.worked_s.all().filter(teacher=t):
                target = user.worked_s.all().filter(teacher=t)[0].teacher
        point = 0
        point = int(request.POST.get('score', ''))
        comment = request.POST.get('comment', '')
        rate = Eval(teacher=target, score=point, details=comment, student=user)
        rate.save()
        return redirect('eval')
    teacher_list = user.worked_s.all()
    eval_list = user.my_eval.all()
    evaluable = []
    for t in teacher_list:
        evaluable.append(t.teacher)
    for e in eval_list:
        if evaluable.count(e.teacher):
            evaluable.remove(e.teacher)
    return render(request, 'User/evaluate.html', {'user': user.user, 'teach': evaluable, 'talkable': talkable})