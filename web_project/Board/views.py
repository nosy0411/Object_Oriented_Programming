from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
# 장고 기본 유저 정보를 가져옴
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def board(request, pg):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    keyw = request.GET.get('keyword', '')
    posts = Post.objects.all().order_by('date').reverse().filter(content__contains=keyw)
    page_count = int(posts.count()/10)+1
    po = []
    onl = timezone.now().today()
    pag = 0
    if keyw == '':      # 키워드 검색 시, 페이지 분리 없음
        for p in posts:
            p.page = int(pag / 10) + 1
            p.save()
            pag += 1
        posts = posts.filter(page=pg)
    else:
        page_count = 1
        for p in posts:
            p.page = 1
            p.save()
    for p in posts:
        if p.date.date().year == onl.year and p.date.date().month == onl.month and p.date.date().day == onl.day:
            po.append([(p.date.strftime('%H:%M')), p])
        else:
            po.append([(p.date.strftime('%y-%m-%d')), p])
    return render(request, 'Board/post_list.html', {'po': po, 'user': user, 'talkable': talkable,'allpage': range(1, page_count+1)})

@login_required
def new_post(request):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date = timezone.now()
            post.state = "대기"
            post.save()
            return redirect('br', pg=1)
    else:
        form = PostForm()
    return render(request, 'Board/post_edit.html', {'form': form, 'user': user, 'talkable': talkable})

@login_required
def my_posts(request):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    posts = Post.objects.all().order_by('date').reverse().filter(author=user)
    po = []
    onl = timezone.now().today()
    for p in posts:
        if p.date.date().year == onl.year and p.date.date().month == onl.month and p.date.date().day == onl.day:
            po.append([(p.date.strftime('%H:%M')), p])
        else:
            po.append([(p.date.strftime('%y-%m-%d')), p])
    return render(request, 'Board/my_post_list.html', {'po': po, 'user': user, 'talkable': talkable})

@login_required
def edit_post(request, pk):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date = timezone.now()
            post.save()
            return redirect('my_post')
    else:
        form = PostForm(instance=post)
    return render(request, 'Board/post_edit.html', {'form': form, 'user': user, 'talkable': talkable})

@login_required
def del_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('my_post')

# 삭제하기전에 html에서 물어보는 것 추가해야 함