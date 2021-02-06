from django.db import models
from django.contrib.auth.models import AbstractUser


class Time(models.Model):
    time = models.TimeField(null=False)


class Hall(models.Model):
    hall_name = models.CharField(max_length=50, verbose_name='공연장 이름')
    hall_lat = models.IntegerField(verbose_name='공연장 위도')
    hall_lng = models.IntegerField(verbose_name='공연장 경도')
    hall_addr = models.TextField(verbose_name='공연장 주소')
    hall_trans = models.TextField(verbose_name='공연장 교통편')


class People(models.Model):
    people_type = models.CharField(max_length=30, verbose_name='직업')
    people_name = models.CharField(max_length=30, verbose_name='이름')


class Show(models.Model):
    TYPE_OF_SHOW = (
        ('play', '연극'),
        ('musical', '뮤지컬'),
    )
    show_type = models.CharField(max_length=20, choices=TYPE_OF_SHOW)
    show_name = models.CharField(max_length=50, verbose_name='공연 이름')
    show_poster = models.ImageField(
        upload_to='idea_image/%Y/%m/%d', verbose_name='공연 포스터', blank=True)
    show_hall = models.ForeignKey(
        Hall, related_name='show_hall', on_delete=models.DO_NOTHING)
    show_date_start = models.DateTimeField(verbose_name='공연 시작일')
    show_date_end = models.DateTimeField(verbose_name='공연 종료일')
    show_runtime = models.TimeField(verbose_name='공연 런타임')
    show_times = models.OneToMany(Time)
    show_intermission = models.TimeField(verbose_name='공연 인터미션')
    show_director = models.ForeignKey(
        People, related_name='show_director', on_delete=models.DO_NOTHING)
    # TODO : show_actor OneToMany로
    show_actor = models.ForeignKey(
        People, related_name='show_actor', on_delete=models.DO_NOTHING)
    show_detail = models.TextField(verbose_name='공연 정보')

# import arrow
# Time(
#     date=arrow.Arrow(year=2021, month=12, day=10, hour=10, minute=30).datetime
# )


class User(AbstractUser):
    grade = models.IntegerField(verbose_name='유저 등급', default=0)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='계정 생성 날짜')
    watched_show = models.ForeignKey(
        Show, related_name='watched_show', verbose_name='관람 공연', on_delete=models.DO_NOTHING, null=True)
    like_people = models.ForeignKey(
        People, related_name='like_people', verbose_name='관심 배우', on_delete=models.DO_NOTHING, null=True)
    interested_show = models.ForeignKey(
        Show, related_name='interested_show', verbose_name='관심 공연', on_delete=models.DO_NOTHING, null=True)


class Review(models.Model):
    review_author = models.ForeignKey(
        User, related_name='review_author', on_delete=models.CASCADE)
    review_show = models.ForeignKey(
        Show, related_name='review_show', on_delete=models.CASCADE)
    review_grade = models.IntegerField(verbose_name='리뷰 별점')
    review_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='리뷰 작성 날짜')
    review_watched_at = models.DateField(verbose_name='작품 관람 날짜')
    review_like = models.IntegerField(verbose_name='리뷰 좋아요 개수', default=0)
    review_content = models.TextField(verbose_name='리뷰 내용', blank=True)
    review_img = models.ImageField(verbose_name='리뷰 사진', blank=True)


class Feed_post(models.Model):
    feed_title = models.CharField(max_length=60, verbose_name='피드 제목')
    feed_author = models.ForeignKey(
        User, related_name='feed_author', on_delete=models.CASCADE)
    feed_content = models.TextField(verbose_name='피드 내용')
    feed_like = models.IntegerField(verbose_name='피드 좋아요 개수', default=0)
    feed_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='피드 생성 날짜')
    TYPE_OF_FEED = (
        ('play_lib', '연극 자유게시판'),
        ('play_inf', '연극 정보게시판'),
        ('musical_lib', '뮤지컬 자유게시판'),
        ('musical_inf', '뮤지컬 정보게시판'),
        ('question', '질문게시판'),
    )
    feed_type = models.CharField(max_length=20, choices=TYPE_OF_FEED)


class Feed_comment(models.Model):
    comment_author = models.ForeignKey(
        User, related_name='comment_author', on_delete=models.CASCADE, verbose_name='작성자')
    comment_content = models.TextField(verbose_name='댓글 내용')
    comment_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='댓글 작성일자')
    comment_post = models.ForeignKey(
        Feed_post, related_name='comment_post', on_delete=models.CASCADE, verbose_name='글제목')
