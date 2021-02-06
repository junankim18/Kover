from django.shortcuts import render
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile


def profile_block(request):
    user = Profile.objects.get(id=request.user.pk)
    pk = user.pk
    shows = user.watched_show.all()
    ctx = {
        'user': user,
        'shows': shows,
    }
    return render(request, 'kover/profile_block.html', ctx)
