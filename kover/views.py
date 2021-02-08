from django.shortcuts import render
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile


def profile_block(request):
    show = Show.objects.all()
    user = Profile.objects.get(id=request.user.pk)
    pk = user.pk
    ctx = {
        'show': show
    }
    return render(request, 'kover/profile_block.html', ctx)


def main(request):
    show = Show.objects.all()
    feed = Feed_post.objects.all()
    num = Feed_post.comment_post
    ctx = {
        'show': show,
        'feed': feed,
        'num': num
    }
    return render(request, 'kover/main.html', ctx)
