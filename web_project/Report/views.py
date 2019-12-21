from django.shortcuts import render, get_object_or_404, redirect
from .models import RepPost
from .forms import RepForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def rep_post(request):
    user = request.user
    talkable = True
    if user.handle.skku:
        if user.handle.line_t.all().filter(alive=True):
            talkable = False
    else:
        if user.handle.line_s.all().filter(alive=True):
            talkable = False
    if request.method == "POST":
        form = RepForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.rep_author = request.user.handle
            post.rep_date = timezone.now()
            post.save()
            return redirect('br', pg=1)
    else:
        form = RepForm()
    return render(request, 'Report/rep_edit.html', {'form': form, 'user': user, 'talkable': talkable})