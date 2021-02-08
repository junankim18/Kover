from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'kover'

urlpatterns = [
    # path('/', views, name='main'),  # 메인 화면)
    path('profile_block/', views.profile_block,
         name='profile_block'),  # 개인 프로필-block),
    # path('profile_geo/', views, name=''),  # 개인 프로필-geo),
    # path('settings/', views, name=''),  # 설정),
    # path('feed/play_inf', views, name=''),  # 연극-정보),
    # path('feed/play_lib', views, name=''),  # 연극-자유),
    # path('feed/musical_inf', views, name=''),  # 뮤지컬-정보),
    # path('feed/musical_lib', views, name=''),  # 뮤지컬-자유),
    # path('feed/', views, name=''),  # 피드-메인),
    # path('feed/question', views,  name=''),  # 질문),
    # path('contents/<int:pk>/', views, name=''),  # 공연별 디테일),
    # path('contents/<int:pk>/comment', views, name=''),  # 공연별 댓글),
    # path('contents/<int:pk>/review', views, name=''),  # 공연별 리뷰),
    # path('contents/', views, name=''),  # 공연 평가할 수 있는 페이지-작품들의 리스트가 뜬다)
    # path('place/<int:pk>/', views, name=''),  # 공연장 디테일),
    # path('search/', views, name=''),  # 검색했을때),
]
