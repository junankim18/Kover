from django.contrib import admin
from django.urls import path, include

app_name = 'kover'

urlpatterns = [
    # name은 url이름과 최대한 같게
    # path('/'  # 메인 화면),
    # path('profile_block/'  # 개인 프로필-block),
    # path('profile_geo/'  # 개인 프로필-geo),
    # path('settings/'  # 설정),
    # path('feed/play_inf'  # 연극-정보),
    # path('feed/play_lib'  # 연극-자유),
    # path('feed/musical_inf'  # 뮤지컬-정보),
    # path('feed/musical_lib'  # 뮤지컬-자유),
    # path('feed/'  # 피드-메인),
    # path('feed/question'  # 질문),
    # path('contents/<int:pk>/'  # 공연별 디테일),
    # path('contents/<int:pk>/comment'  # 공연별 댓글),
    # path('contents/<int:pk>/review'  # 공연별 리뷰),
    # path('contents/'  # 공연 평가할 수 있는 페이지-작품들의 리스트가 뜬다)
    # path('place/<int:pk>/'  # 공연장 디테일),
    # path('search/'  # 검색했을때),
]
