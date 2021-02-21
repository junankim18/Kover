from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .models import User, Show, People, Review, Feed_post, Feed_comment, Profile
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
from dateutil.parser import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# profile_block : 기본 프로필페이지


@login_required
def profile_block(request):
    users = Profile.objects.get(user=request.user)
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


# main : 메인 페이지


def main(request):
    username = Profile.objects.filter(id=request.user.id)
    if username:
        actors = username[0].like_actor.all().order_by('people_name')
    else:
        actors = []

    show_1 = Show.objects.all().order_by('-show_date_start')[:5]  # 작품 최신 순
    show_2 = Show.objects.all().order_by('-show_date_start')[:5]  # 작품 리뷰 많은 순

    feed_1 = Feed_post.objects.all().order_by(
        '-feed_created_at')[:5]  # 피드 최신 순
    feed_2 = Feed_post.objects.all().order_by('-feed_like')[:5]  # 피드 좋아요 많은 순

    actorshow = []
    wantshow = []
    for actor in actors:
        for show in actor.show_actor.all():
            actorshow.append(show)

    for j in actorshow:
        if j not in wantshow:
            wantshow.append(j)

    ctx = {
        'show_1': show_1,
        'show_2': show_2,
        'feed_1': feed_1,
        'feed_2': feed_2,
        'wantshow': wantshow,
    }
    return render(request, 'kover/main.html', ctx)


# profile_geo : 지도 프로필 페이지


@login_required
def profile_geo(request):
    shows = Show.objects.all()
    ctx = {
        'shows': shows
    }
    return render(request, 'kover/profile_geo.html', ctx)


def feed_main(request):
    feeds = Feed_post.objects.all()
    # feed_0 = Feed_post.objects.all().order_by('-feed_like')[:5]
    feed_0 = Feed_post.objects.all()[:5]  # 피드 좋아요 많은 순
    feed_1 = Feed_post.objects.filter(feed_type='play_lib').order_by(
        '-feed_created_at')[:5]  # 연극-자유
    feed_2 = Feed_post.objects.filter(feed_type='play_inf').order_by(
        '-feed_created_at')[:5]  # 연극-정보
    feed_3 = Feed_post.objects.filter(feed_type='musical_lib').order_by(
        '-feed_created_at')[:5]  # 뮤지컬-자유
    feed_4 = Feed_post.objects.filter(feed_type='musical_inf').order_by(
        '-feed_created_at')[:5]  # 뮤지컬-정보
    feed_5 = Feed_post.objects.filter(feed_type='question').order_by(
        '-feed_created_at')[:5]  # 질문
    # n = Feed_comment.objects.count()
    comment_list = Feed_comment.objects.all()

    comlist = []
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))

    ctx = {
        'feeds': feeds,
        'feed_0': feed_0,
        'feed_1': feed_1,
        'feed_2': feed_2,
        'feed_3': feed_3,
        'feed_4': feed_4,
        'feed_5': feed_5,
        'comlist': comlist
    }
    return render(request, 'kover/feed_main.html', ctx)




def feed_page(request, pk):
    if request.user not in User.objects.all():
        users = 0
    else:
        users = Profile.objects.filter(user=request.user)
        users = users[0]
        # feeds= Feed_post.objects.all()
    id = users.pk
    feed = Feed_post.objects.get(pk=pk)
    print(users in feed.feed_like.all())
    comlist = []
    # for feed in feeds:
    comlist.append(len(feed.comment_post.all()))
    ctx = {
        'users': users,
        'feed': feed,
        'comlist': comlist
    }
    return render(request, 'kover/feed_page.html', ctx)


def feed_create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)       
        if form.is_valid():
            post = form.save()
            return redirect('kover:play_lib')
    else: 
        form = PostForm()
        ctx = {'form':form}
        return render(request, 'kover/feed_form.html', ctx)


def feed_update_post(request, pk):
    post = get_object_or_404(Feed_post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post=form.save()
            return redirect('kover:feed_page', pk) 
    else:
        form = PostForm(instance=post)
        ctx={'form':form}
        return render(request, 'kover/feed_form.html', ctx)


def feed_delete_post(request, pk):
    post = get_object_or_404(Feed_post, pk=pk)
    if request.method == 'GET':
        return redirect('kover:feed_page', post.id)

    elif request.method == 'POST':
        post.delete()
        return redirect('kover:play_lib')


def feed_musical_lib(request):
    feed = Feed_post.objects.filter(feed_type='musical_lib')
    feeds = Feed_post.objects.filter(feed_type='musical_lib').order_by(
        '-feed_created_at')[:]  # 피드 최신 순
    comlist = []
    paginator = Paginator(feeds, 3)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.get_page(page)
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feed': feed,
        'feeds': feeds,
        'comlist': comlist,
        'posts': posts,
    }
    return render(request, 'kover/feed_board.html', ctx)


def feed_musical_inf(request):
    # feed= Feed_post.objects.all()
    # feed = Feed_post.objects.get(pk=pk)
    feed = Feed_post.objects.filter(feed_type='musical_inf')
    feeds = Feed_post.objects.filter(feed_type='musical_inf').order_by(
        '-feed_created_at')[:]  # 피드 최신 순
    comlist = []
    paginator = Paginator(feeds, 3)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.get_page(page)
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feed': feed,
        'feeds': feeds,
        'comlist': comlist,
        'posts': posts,
    }
    return render(request, 'kover/feed_board.html', ctx)


def feed_play_lib(request):
    feed = Feed_post.objects.filter(feed_type='play_lib')
    feeds = Feed_post.objects.filter(feed_type='play_lib').order_by(
        '-feed_created_at')[:]  # 피드 최신 순
    comlist = []
    paginator = Paginator(feeds, 3)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.get_page(page)
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feed': feed,
        'feeds': feeds,
        'comlist': comlist,
        'posts': posts,
    }
    return render(request, 'kover/feed_board.html', ctx)


def feed_play_inf(request):
    feed = Feed_post.objects.filter(feed_type='play_inf')
    feeds = Feed_post.objects.filter(feed_type='play_inf').order_by(
        '-feed_created_at')[:]  # 피드 최신 순
    comlist = []
    paginator = Paginator(feeds, 3)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.get_page(page)
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feed': feed,
        'feeds': feeds,
        'comlist': comlist,
        'posts': posts,
    }
    return render(request, 'kover/feed_board.html', ctx)


def feed_question(request):
    feed = Feed_post.objects.filter(feed_type='question')
    feeds = Feed_post.objects.filter(feed_type='question').order_by(
        '-feed_created_at')[:]  # 피드 최신 순
    comlist = []
    paginator = Paginator(feeds, 3)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.get_page(page)
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feed': feed,
        'feeds': feeds,
        'comlist': comlist,
        'posts': posts,
    }
    return render(request, 'kover/feed_board.html', ctx)


def feed_hot_feed(request):
    feed = Feed_post.objects.all()
    feeds = Feed_post.objects.all().order_by('-feed_like')[:]
    # 피드 좋아요 많은 순
    comlist = []
    paginator = Paginator(feeds, 3)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.get_page(page)
    for feed in feeds:
        comlist.append(len(feed.comment_post.all()))
    ctx = {
        'feed': feed,
        'feeds': feeds,
        'comlist': comlist,
        'posts': posts,
    }
    return render(request, 'kover/feed_hot.html', ctx)


# show_detail : contents 상세보기 페이지


def show_detail(request, pk):
    username = Profile.objects.filter(user=request.user)
    show = Show.objects.get(id=pk)
    peoples = People.objects.all()
    reviews = show.review_show.all().order_by('-id')
    star_rate_reviews = []
    for review in reviews:
        if review.review_content == '.':
            star_rate_reviews.append(review)
    revnum = len(reviews)-len(star_rate_reviews)

    show_times = show.show_times.all()
    showdatelist = []
    delta = (show.show_date_end - show.show_date_start).days
    for i in range(delta):
        showdatelist.append(datetime.date(
            show.show_date_start) + timedelta(days=i))
    mygrade = 0
    if username:
        for rev in username[0].review_author.all():
            if show.id == rev.review_show.id:
                mygrade = rev.review_grade
        username = username[0]
    ctx = {
        'username': username,
        'pk': pk,
        'show': show,
        'peoples': peoples,
        'reviews': reviews,
        'revnum': revnum,
        'show_times': show_times,
        'mygrade': mygrade,
        'showdatelist': showdatelist,
    }
    return render(request, 'kover/show_detail.html', ctx)


# press_like : feed 페이지에서 좋아요를 눌렀을 때

@ method_decorator(csrf_exempt)
def press_like(request):
    if request.method == 'GET':
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(request, 'kover/feed_layout.html', ctx)
    elif request.method == 'POST':
        users = Profile.objects.get(user=request.user)
        request = json.loads(request.body)
        feed_id = request['id']
        feed = Feed_post.objects.get(id=feed_id)
        feed.feed_like.add(users)
        feed.save()
        return JsonResponse({'id': feed_id})

# press_dislike : feed 페이지에서 좋아요를 눌렀을 때


@ method_decorator(csrf_exempt)
def press_dislike(drequest):
    if drequest.method == 'GET':
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(drequest, 'kover/feed_layout.html', ctx)
    elif drequest.method == 'POST':
        liketype = False
        request = json.loads(drequest.body)
        feed_id = request['id']
        feed = Feed_post.objects.get(id=feed_id)
        feed.feed_like -= 1
        feed.save()
        return JsonResponse({'id': feed_id, 'liketype': liketype})

# press_com : feed 페이지에서 게시를 눌렀을 때


@ method_decorator(csrf_exempt)
def press_com(comrequest):
    if comrequest.method == 'GET':
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(comrequest, 'kover/feed_layout.html', ctx)
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
                                   comment_content=content, comment_post=feed,
                                   )
            comment.save()
        return JsonResponse({'id': feed_id, 'comment': comment.comment_content, 'writer': user.nickname, 'time':comment.comment_created_at})


# create_watched_show : 네비게이션 바에서  '리뷰등록'을 눌렀을 때, 아직 평가하지 않은 작품들의 리스트가 나온다

@ login_required
def create_watched_show(request):
    users = Profile.objects.filter(user=request.user)
    users = users[0]
    watchedshows = users.watched_show.all()
    shows = Show.objects.all()
    unwatchedplays = []
    unwatchedmusicals = []
    for show in shows:
        if show not in watchedshows and show not in unwatchedplays and show.show_type == 'play':
            unwatchedplays.append(show)
        elif show not in watchedshows and show not in unwatchedmusicals and show.show_type == 'musical':
            unwatchedmusicals.append(show)

            # plays = Show.objects.filter(Q(show_type='play'))
            # musicals = Show.objects.filter(Q(show_type='musical'))
    ctx = {
        'users': users,
        'plays': unwatchedplays,
        'musicals': unwatchedmusicals
    }
    return render(request, 'kover/watched_show.html', ctx)


# create_review : contents detail 페이지에서 '내 리뷰 등록하기'를 눌렀을 때


@ method_decorator(csrf_exempt)
def create_review(comrequest):
    if comrequest.method == 'GET':
        return render(comrequest, 'kover/show_detail.html')
    elif comrequest.method == 'POST':
        request = json.loads(comrequest.body)
        show_id = request['id']
        content = request['content']
        star = request['star']
        seldate = request['seldate']
        yyyy = seldate[:4]
        mm = seldate[5:9]
        dd = seldate[-3:]
        mm = mm.strip()
        dd = dd.strip()
        if len(mm) == 2:
            mm = '0'+mm[:1]
        elif len(mm) == 3:
            mm = mm[:2]
        if len(dd) == 2:
            dd = '0'+dd[:1]
        elif len(dd) == 3:
            dd = dd[:2]
        date = yyyy+'-'+mm+'-'+dd
        show = Show.objects.get(id=show_id)
        user_id = comrequest.user
        print('here?')
        print('here?')
        print('here?')
        print('here?')
        print('here?')
        user = Profile.objects.get(user=user_id)
        nickname = user.nickname
        if content:
            myreviews = Review.objects.filter(review_author=user)
            for myreview in myreviews:
                if myreview.review_show == show:
                    review = myreview
            review.review_author = user
            review.review_show = show
            review.review_grade = star
            review.review_watched_at = date
            review.review_content = content
            review.save()
        return JsonResponse({'id': show_id,
                             'comment': review.review_content,
                             'writer': user.nickname,
                             'date': review.review_watched_at,
                             'grade': review.review_grade,
                             'yyyy': yyyy,
                             'mm': mm,
                             'dd': dd,
                             })


# star_rate : contents detail 페이지에서 별점을 눌렀을 때


@ method_decorator(csrf_exempt)
def star_rate(starrequest):
    if starrequest.method == 'GET':
        return render(starrequest, 'kover/show_detail.html')
    elif starrequest.method == 'POST':
        request = json.loads(starrequest.body)
        show_id = request['show_id']
        star_rate = request['value']
        user_id = starrequest.user
        user = Profile.objects.get(user=user_id)
        show = Show.objects.get(id=show_id)
        review = 0
        myreviews = Review.objects.filter(review_author=user)

        for myreview in myreviews:
            if myreview.review_show == show:
                review = myreview

        if review == 0:
            review = Review(
                review_author=user,
                review_show=show,
                review_grade=star_rate,
                review_watched_at='2999-12-31',
                review_content='.'
            )
            review.save()
            user.watched_show.add(show)
        else:
            review.review_grade = star_rate
            review.save()

        return JsonResponse({'show_id': show_id,
                             'writer': user.nickname,
                             'star_rate': review.review_grade,
                             })


def searchResult(request):

    show_result = Show.objects.all()
    people_result = People.objects.all()
    feed_result = Feed_post.objects.all()

    q = request.GET.get('q')

    if q:
        show_result = show_result.filter(
            Q(show_name__icontains=q) |
            Q(show_detail__icontains=q)
        ).distinct()

        people_result = people_result.filter(
            Q(people_name__icontains=q)
        ).distinct()

        feed_result = feed_result.filter(
            Q(feed_title__icontains=q) |
            Q(feed_author__nickname__icontains=q) |
            Q(feed_content__icontains=q)
        ).distinct()

    shows = Show.objects.all()
    show_result = list(show_result)

    for show in shows:
        for people in people_result:
            if people in show.show_actor.all():
                show_result.append(show)

    ctx = {
        'q': q,
        'show_result': show_result,
        'people_result': people_result,
        'feed_result': feed_result,
    }

    return render(request, 'kover/search.html', ctx)


@method_decorator(csrf_exempt)
def delete_review(delrequest):
    if delrequest.method == 'GET':
        show_list = Show.objects.all()
        ctx = {"shows": show_list}
        return render(delrequest, 'kover/show_detail.html', ctx)
    elif delrequest.method == 'POST':
        request = json.loads(delrequest.body)
        show_id = request['show_id']
        review_id = request['review_id']
        show = Show.objects.get(id=show_id)
        review = Review.objects.get(id=review_id)
        review.delete()
        return JsonResponse({'show_id': show_id, 'review_id': review_id})
