# 장고 기본 유저 정보를 가져옴
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core import validators
from django import forms
from .models import Line, Profile

class SignupForm(forms.Form):
    
    email = forms.EmailField(required=True, label="이메일",
                            help_text="이메일 형식으로 입력해 주세요. 이메일은 아이디와 비밀번호를 찾을때 이용됩니다.\n"
                                        "단, 과외 대상 학생이 아닌 과외 선생님으로 활동하려면,\n"
                                        "성대 이메일을 적고 메일 인증을 거쳐야 활동할 수 있습니다.", 
                            )

    username = forms.RegexField(required=True, label="사용자 이름",max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text="30개보다 작은 숫자나 문자 그리고 @/./+/-/_ 만 입력하실 수 있습니다.",
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                    '유효한 사용자 이름을 입력하세요.'),
                                    ],
                                error_messages={'unique': "이미 존재하는 사용자 이름입니다."},
                                )
                                    
    password1 = forms.CharField(required=True, label="비밀번호",
                                help_text="비밀번호를 입력해 주세요.",
                                widget=forms.PasswordInput())


    password2 = forms.CharField(required=True, label="비밀번호 확인",
                                help_text="비밀번호를 다시 한번 입력해 주세요.",
                                widget=forms.PasswordInput())

    last_name = forms.CharField(required=True, label="성", help_text="프로필에 표시될 성을 입력하세요")
    first_name = forms.CharField(required=True, label="이름", help_text="프로필에 표시될 이름을 입력하세요")



    field_order=['email','username','password1','password2','last_name','first_name']

    def clean(self):
        clean_data=super().clean()
        # This method will set the cleaned_data attribute
        email = clean_data.get('email')
        username = clean_data.get('username')
        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "이미 존재하는 이메일 입니다.")

        if User.objects.filter(username=username).exists():
            self.add_error('username', "이미 존재하는 이름입니다.")
        
        if not password1 == password2:
            self.add_error('password2', '비밀번호가 서로 일치하지 않습니다.')
        
        return self.cleaned_data

    class Meta:
        User = get_user_model()
        model = User
        fields = ['email','username','password1','last_name','first_name']

    # def save(self, commit=True): # 저장하는 부분 오버라이딩
    #     user = super(SignupForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user


class SigninForm(forms.Form): #로그인을 제공하는 class이다.
    username = forms.CharField(label="사용자 이름", max_length=30)
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput())

    def clean(self):
        clean_data=super().clean()
        # This method will set the cleaned_data attribute
        username = clean_data.get('username')
        password = clean_data.get('password')

        if username and password:
            
            if not User.objects.filter(username=username).exists():
                self.add_error('username', "존재하지 않는 사용자입니다.")    
            else:
                user = User.objects.get(username=username)
                if not check_password(password, user.password):
                    self.add_error('password','비밀번호가 틀렸습니다.')

        return self.cleaned_data

class ResendForm(forms.Form):
    email = forms.EmailField(required=True, label="이메일")

    def clean(self):
        clean_data=super().clean()

        email=clean_data.get('email')
        if not User.objects.filter(email=email).exists():
            self.add_error('email', "등록되지 않은 이메일 입니다.")  
        return self.cleaned_data


class ResetForm(forms.Form):
    password = forms.CharField(label="비밀번호 재설정", widget=forms.PasswordInput())

    def clean(self):
        clean_data=super().clean()
        # This method will set the cleaned_data attribute
        
        password = clean_data.get('password')

        return self.cleaned_data


class LineForm(forms.ModelForm):

    class Meta:
        model = Line
        fields = ('content',)


class ProfForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('is_male', 'age', 'intro', 'subj', 'region', 'dep')
