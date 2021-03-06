from django.contrib import admin
from django.urls import path, include
from . import views
# from . import crawling

app_name = 'kover'

urlpatterns = [
    path('', views.main, name='main'),  # 메인 화면)
    path('profile_block/', views.profile_block,
         name='profile_block'),  # 개인 프로필-block),
    path('profile_geo/', views.profile_geo,
         name='profile_geo'),  # 개인 프로필-geo),
    # path('settings/', views, name=''),  # 설정),
    # path('feed/play_inf', views, name=''),  # 연극-정보),
    path('feed/', views.feed_main, name='feed_main'),  # 피드-메인),
    path('feed/delete/', views.delete_comment, name='delete_comment'),
    path('feed/like/', views.press_like, name='press_like'),
    path('feed/dislike/', views.press_dislike, name='press_dislike'),
    path('feed/comment/', views.press_com, name='press_com'),  # 피드-댓글),
    path('feed/page/<int:pk>/', views.feed_page,
         name='feed_page'),  # 피드-게시물 하나의 상세 페이지),
    path('feed/post/', views.feed_create_post,
         name='create'),  # 피드 글 작성),
    path('feed/edit/<int:pk>/', views.feed_update_post,
         name='update'),  # 피드 글 수정),
    path('feed/delete/<int:pk>/', views.feed_delete_post,
         name='delete'),  # 피드 글 삭제),
    path('feed/play_inf/', views.feed_play_inf, name='play_lib'),  # 연극-정보),
    path('feed/play_lib/', views.feed_play_lib, name='play_lib'),  # 연극-자유),
    path('feed/musical_inf/', views.feed_musical_inf,
         name='musical_inf'),  # 뮤지컬-정보),
    path('feed/musical_lib/', views.feed_musical_lib,
         name='musical_lib'),  # 뮤지컬-자유),
    path('feed/question/', views.feed_question, name='feed_question'),  # 질문),
    path('feed/hot_feed/', views.feed_hot_feed,
         name='feed_hot_feed'),  # hot 피드),

    path('contents/<int:pk>/', views.show_detail,
         name='show_detail'),  # 공연별 디테일),
    path('contents/<int:pk>/', views.show_detail,
         name='show_detail'),  # 공연별 댓글),
    # path('contents/<int:pk>/review', views, name=''),  # 공연별 리뷰),
    # 공연 평가할 수 있는 페이지-작품들의 리스트가 뜬다)
    path('actors/', views.create_like_actor, name='create_like_actor'),
    path('actors/like/', views.click_like_actor, name='click_like_actor'),
    path('actors/unlike/', views.click_unlike_actor, name='click_unlike_actor'),
    path('contents/', views.create_watched_show, name='create_watched_show'),
    path('contents/like/', views.create_fav_show, name='create_fav_show'),
    path('contents/unlike/', views.delete_fav_show, name='delete_fav_show'),
    path('contents/rate/', views.star_rate, name='star_rate'),
    path('contents/review/', views.create_review,
         name='create_review'),  # 작품별 댓글달기 기능
    # path('place/<int:pk>/', views, name=''),  # 공연장 디테일),
    path('search/', views.searchResult, name='searchResult'),  # 검색했을때),
    # path('crawl/people/', crawling.crawlpeople, name='crawlpeople'),  # 인물크롤링
    # path('crawl/place/', crawling.crawlplace, name='crawlplace'),  # 장소크롤링
    path('contents/delete/', views.delete_review,
         name='delete_review')  # 작품별 댓글 삭제
]
