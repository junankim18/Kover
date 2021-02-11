from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .forms import ShowForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def profile_block(request):
    users = Profile.objects.get(id=request.user.pk)
    pk = users.pk
    shows = users.watched_show.all()
    actors = users.like_actor.all().order_by('people_name')
    favorites = users.interested_show.all()
    reviews = users.review_author.all().order_by('-id')
    showlist = list(shows)
    hallnum = len(showlist)
    halllist = []  # 공연장 리스트
    wantlist = []  # 공연장 리스트중에서 중복된 값 제거
    renum = {}  # 공연장 리스트중에서 중복된 값 카운트

    # 공연장 리스트
    for i in range(hallnum):
        halllist.append(showlist[i].show_hall)

    # 중복된 리스트의 요소 제거
    for i in halllist:
        if i not in wantlist:
            wantlist.append(i)

    overlapnum = len(wantlist)

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
        'users': users,
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
    # try:
    #     username = Profile.objects.get(pk=request.user.pk)
    # except Profile.DoesNotExist:
    #     username = None
    username = Profile.objects.filter(id=request.user.id)
    if username:
        actors = username.like_actor.all().order_by('people_name')
    else:
        actors = []

    show_1 = Show.objects.all().order_by('-show_date_start')[:5]  # 작품 최신 순
    show_2 = Show.objects.all().order_by('-show_date_start')[:5]  # 작품 리뷰 많은 순

    feed_1 = Feed_post.objects.all().order_by(
        '-feed_created_at')[:5]  # 피드 최신 순
    feed_2 = Feed_post.objects.all().order_by('-feed_like')[:5]  # 피드 좋아요 많은 순

    commentlist = []
    for feedind in feed_2:
        commentlist.append(len(feedind.comment_post.all()))

    actorshow = []
    wantshow = []
    for actor in actors:
        for show in actor.show_actor.all():
            actorshow.append(show)

    for j in actorshow:
        if j not in wantshow:
            wantshow.append(j)

    print(wantshow)

    ctx = {
        'show_1': show_1,
        'show_2': show_2,
        'feed_1': feed_1,
        'feed_2': feed_2,
        'commentlist': commentlist,
        'wantshow': wantshow,
    }
    return render(request, 'kover/main.html', ctx)


def profile_geo(request):
    shows = Show.objects.all()
    ctx = {
        'shows': shows
    }
    return render(request, 'kover/profile_geo.html', ctx)


def feed_page(request):
    feeds = Feed_post.objects.all()
    comlist = []
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feeds': feeds,
        'comlist': comlist
    }
    return render(request, 'kover/feed_layout.html', ctx)


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


@ method_decorator(csrf_exempt)
def press_like(request):
    if request.method == 'GET':
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(request, 'insta/feed_layout.html', ctx)
    elif request.method == 'POST':
        request = json.loads(request.body)
        feed_id = request['id']
        feed = Feed_post.objects.get(id=feed_id)
        feed.feed_like += 1
        feed.save()
        return JsonResponse({'id': feed_id})


@ method_decorator(csrf_exempt)
def press_com(comrequest):
    if comrequest.method == 'GET':
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(comrequest, 'insta/feed_layout.html', ctx)
    elif comrequest.method == 'POST':
        request = json.loads(comrequest.body)
        feed_id = request['id']
        content = request['content']
        feed = Feed_post.objects.get(id=feed_id)
        user_id = comrequest.user.id
        user = Profile.objects.get(id=user_id)
        nickname = user.nickname
        if content:
            comment = Feed_comment(comment_author=user,
                                   comment_content=content, comment_post=feed)
            comment.save()
        return JsonResponse({'id': feed_id, 'comment': comment.comment_content, 'writer': user.nickname})


def create_watched_show(request):
    if request.method == 'POST':
        form = ShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save()
            new_pk = show.id
            return redirect('kover:profile_block', new_pk)
    elif request.method == 'GET':
        form = ShowForm()
        ctx = {
            'form': form
        }
        return render(request, 'kover/watched_show.html', ctx)
