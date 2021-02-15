from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'kover'

urlpatterns = [
    path('', views.main, name='main'),  # 메인 화면)
    path('profile_block/', views.profile_block,
         name='profile_block'),  # 개인 프로필-block),
    path('profile_geo/', views.profile_geo,
         name='profile_geo'),  # 개인 프로필-geo),
    # path('settings/', views, name=''),  # 설정),
    # path('feed/play_inf', views, name=''),  # 연극-정보),
    # path('feed/play_lib', views, name=''),  # 연극-자유),
    # path('feed/musical_inf', views, name=''),  # 뮤지컬-정보),
    path('feed/musical_lib', views.feed_musical_lib, name='feed_musical_lib'),  # 뮤지컬-자유),
    path('feed/', views.feed_page, name='feed_main'),  # 피드-메인),
    path('feed/like/', views.press_like, name='press_like'),  # 피드-메인),
    path('feed/comment/', views.press_com, name='press_com'),  # 피드-메인),
    # path('feed/question', views,  name=''),  # 질문),
    path('contents/<int:pk>/', views.show_detail,
         name='show_detail'),  # 공연별 디테일),
    path('contents/<int:pk>/', views.show_detail,
         name='show_detail'),  # 공연별 댓글),
    # path('contents/<int:pk>/review', views, name=''),  # 공연별 리뷰),
    # 공연 평가할 수 있는 페이지-작품들의 리스트가 뜬다)
    path('contents/', views.create_watched_show, name='create_watched_show'),
    path('contents/review/', views.create_review,
         name='create_review'),  # 작품별 댓글달기 기능
    # path('place/<int:pk>/', views, name=''),  # 공연장 디테일),
    # path('search/', views, name=''),  # 검색했을때),
]




