#import arrow
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Time(models.Model):
    time = models.DateTimeField(null=True)


# 나중에 크롤링할때 이런 형식으로 show에 맞는 time 넣어주기
# Time(
#     time=arrow.Arrow(year=2021, month=12, day=10, hour=10, minute=30).datetime
# )


class Hall(models.Model):
    hall_name = models.CharField(max_length=50, verbose_name='공연장 이름')
    hall_lat = models.FloatField(verbose_name='공연장 위도')
    hall_lng = models.FloatField(verbose_name='공연장 경도')
    hall_addr = models.TextField(verbose_name='공연장 주소')
    hall_trans = models.TextField(verbose_name='공연장 교통편', blank=True)

    def __str__(self):
        return self.hall_name


class People(models.Model):
    people_type = models.CharField(max_length=30, verbose_name='직업')
    people_name = models.CharField(max_length=30, verbose_name='이름')
    people_img = models.ImageField(
        upload_to='people_image/%Y/%m/%d', verbose_name='배우 사진', blank=True)
    people_birth = models.DateField(verbose_name='생년월일', null=True)

    def __str__(self):
        return self.people_name


class Show(models.Model):
    TYPE_OF_SHOW = (
        ('play', '연극'),
        ('musical', '뮤지컬'),
    )
    show_type = models.CharField(max_length=20, choices=TYPE_OF_SHOW)
    show_name = models.CharField(max_length=50, verbose_name='공연 이름')
    show_poster = models.ImageField(
        upload_to='poster_image/%Y/%m/%d', verbose_name='공연 포스터', blank=True)
    show_hall = models.ForeignKey(
        Hall, related_name='show_hall', on_delete=models.DO_NOTHING)
    show_date_start = models.DateTimeField(verbose_name='공연 시작일', null=True)
    show_date_end = models.DateTimeField(verbose_name='공연 종료일', null=True)
    show_runtime = models.DurationField(
        default="02:50:00", verbose_name='공연 런타임', null=True)
    show_times = models.ManyToManyField(Time, related_name='show_time')
    show_intermission = models.DurationField(
        default="00:20:00", verbose_name='공연 인터미션', null=True)
    show_director = models.ForeignKey(
        People, related_name='show_director', on_delete=models.DO_NOTHING)
    show_actor = models.ManyToManyField(People, related_name='show_actor')
    show_detail = models.TextField(verbose_name='공연 정보')

    def __str__(self):
        return self.show_name


class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings',
        blank=True,
    )


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, verbose_name='유저닉네임')
    grade = models.IntegerField(verbose_name='유저 등급', default=0)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='계정 생성 날짜')
    profileimg = models.ImageField(
        upload_to='profile_image/%Y/%m/%d', verbose_name='프로필 이미지', blank=True)
    watched_show = models.ManyToManyField(
        Show, related_name='watched_show', verbose_name='관람 공연')
    like_actor = models.ManyToManyField(
        People, related_name='like_people', verbose_name='관심 배우')
    interested_show = models.ManyToManyField(
        Show, related_name='interested_show', verbose_name='관심 공연')
    bio = models.TextField(verbose_name='자기 소개', blank=True)
    biolink = models.URLField(verbose_name='자기 사이트', blank=True)

    def __str__(self):
        return self.nickname


class Review(models.Model):
    review_author = models.ForeignKey(
        Profile, related_name='review_author', on_delete=models.CASCADE)
    review_show = models.ForeignKey(
        Show, related_name='review_show', on_delete=models.CASCADE)
    review_grade = models.IntegerField(verbose_name='리뷰 별점')
    review_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='리뷰 작성 날짜')
    review_watched_at = models.DateField(verbose_name='작품 관람 날짜')
    review_like = models.IntegerField(verbose_name='리뷰 좋아요 개수', default=0)
    review_content = models.TextField(verbose_name='리뷰 내용', blank=True)
    review_img = models.ImageField(verbose_name='리뷰 사진', blank=True)

    def __str__(self):
        return self.review_content


class Feed_post(models.Model):
    feed_title = models.CharField(max_length=60, verbose_name='피드 제목')
    feed_author = models.ForeignKey(
        Profile, related_name='feed_author', on_delete=models.CASCADE)
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
        Profile, related_name='comment_author', on_delete=models.CASCADE, verbose_name='작성자')
    comment_content = models.TextField(verbose_name='댓글 내용')
    comment_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='댓글 작성일자')
    comment_post = models.ForeignKey(
        Feed_post, related_name='comment_post', on_delete=models.CASCADE, verbose_name='글제목')
