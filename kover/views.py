from django.shortcuts import render
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile


def profile_block(request):
    user = Profile.objects.get(id=request.user.pk)
    pk = user.pk
    shows = user.watched_show.all()
    actors = user.like_actor.all()
    favorites = user.interested_show.all()
    reviews = user.review_author.all().order_by('-id')
    ctx = {
        'user': user,
        'shows': shows,
        'actors': actors,
        'favorites': favorites,
        'reviews': reviews
    }
    return render(request, 'kover/profile_block.html', ctx)
