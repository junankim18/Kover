from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .forms import ShowForm


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
    shows = Show.objects.all()
    ctx = {
        'shows': shows
    }
    return render(request, 'kover/profile_geo.html', ctx)


def feed_page(request):
    feeds = Feed_post.objects.all()
    ctx = {
        'feeds': feeds
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


@method_decorator(csrf_exempt)
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


@method_decorator(csrf_exempt)
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
