from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # 로그인 모듈만 따로 쓸때. 회원가입 및 로그인 연동안됨. login.html에 template구현되어 있음. 즉 login.html은 최종적으로 안씀
    # path('', include('django.contrib.auth.urls')),   
    path('profile/id=<int:pk>', views.user_prof, name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout",kwargs={'next_page': '/'}),   
    path('', views.signin, name='signin'),
    path('login/', views.signin, name='signin'),
    path('registration/', views.signup, name='signup'),
    path('registration/signup_ok', views.signup_ok, name='signup_ok'),
    path('registration/verification', views.verification, name='verification'),
    path('registration/verification_resend', views.verification_resend, name='verification_resend'),
    path('registration/resend', views.resend, name='resend'),
    path('registration/change', views.change_pw, name='change_pw'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    re_path(r'^rechange/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.email_change_pw, name='email_change_pw'),
    path('1to1-<int:pk>', views.ask_to_talk, name='1to1'),
    path('1to1/my', views.personal, name='personal'),
    path('refuse', views.line_ref, name='refuse'),
    path('consent', views.line_consent, name='consent'),
    path('eval', views.eval, name='eval'),
    path('profile/<int:pk>/modify', views.revise_prof, name='prof_mod')
]
