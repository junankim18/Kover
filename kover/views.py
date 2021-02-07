from django.shortcuts import render
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile


def profile_block(request):
    user = Profile.objects.get(id=request.user.pk)
    pk = user.pk
    shows = user.watched_show.all()
    actors = user.like_actor.all()
    favorites = user.interested_show.all()
    reviews = user.review_author.all().order_by('-id')
    showlist = list(shows)
    hallnum = len(showlist)
    wantlist = []
    print(showlist)
    print(showlist[0].show_hall)
    print(showlist[1].show_hall)
    print(showlist[2].show_hall)
    if showlist[0].show_hall == showlist[2].show_hall:
        print('같다')

    for i in range(hallnum):
        for j in range(hallnum):
            if i >= j:
                pass
            elif showlist[i].show_hall == showlist[j].show_hall:
                pass
            else:
                wantlist.append(showlist[i])

    overlapnum = len(wantlist)

    ctx = {
        'user': user,
        'shows': shows,
        'actors': actors,
        'favorites': favorites,
        'reviews': reviews,
        'showlist': showlist,
        'hallnum': hallnum,
        'overlapnum': overlapnum,
        'wantlist': wantlist,

    }
    return render(request, 'kover/profile_block.html', ctx)
