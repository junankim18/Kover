from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

def profile_block(request):
    user = Profile.objects.get(id=request.user.pk)
    pk = user.pk
    shows = user.watched_show.all()
    actors = user.like_actor.all().order_by('people_name')
    favorites = user.interested_show.all()
    reviews = user.review_author.all().order_by('-id')
    showlist = list(shows)
    hallnum = len(showlist)
    halllist = []  # 공연장 리스트
    wantlist = []  # 공연장 리스트중에서 중복된 값 제거
    renum = {}  # 공연장 리스트중에서 중복된 값 카운트

    # 중복된 리스트의 요소 제거
    for i in range(hallnum):
        for j in range(hallnum):
            if i >= j:
                pass
            elif showlist[i].show_hall == showlist[j].show_hall:
                pass
            else:
                wantlist.append(showlist[i])
    overlapnum = len(wantlist)

    # 공연장 리스트
    for i in range(hallnum):
        halllist.append(showlist[i].show_hall)

    for i in halllist:
        try:
            renum[i] += 1
        except:
            renum[i] = 1

    mostvisitnum = 0
    for i in renum.values():
        if i > mostvisitnum:
            mostvisitnum = i
        else:
            pass

    # // {'AA': '0', 'BB': '1', 'CC': '2'}
    reversedict = {v: k for k, v in renum.items()}
    hallname = reversedict.get(mostvisitnum)

    ctx = {
        'user': user,
        'shows': shows,
        'actors': actors,
        'favorites': favorites,
        'reviews': reviews,
        'showlist': showlist,
        'overlapnum': overlapnum,
        'wantlist': wantlist,
        'hallname': hallname,
        'mostvisitnum': mostvisitnum

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


def profile_geo(request):
    return render(request, 'kover/profile_geo.html')


def show_detail(request, pk):
    show = Show.objects.get(id=pk)
    peoples = People.objects.all()
    reviews = show.review_show.all()
    ctx = {
        'pk': pk,
        'show': show,
        'peoples': peoples,
        'reviews': reviews,
    }
    return render(request, 'kover/show_detail.html', ctx)




class Feed(View):
    template_name = 'kover/feed_layout.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Feed, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(request, self.template_name, ctx)

    def post(self, request):
        request = json.loads(request.body)
        feed_id = request['id']
        button_type = request['type']
        feed = Feed_post.objects.get(id=feed_id)
        comment = Feed_comment.objects.get(id=feed_id)
        if button_type == 'feed_like':
            feed_like = feed_like + 1
        Feed_post.save()

        return JsonResponse({'id': feed_id, 'type':feed_like})


