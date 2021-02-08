from django.shortcuts import render
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile

def show_detail(request, pk):
    shows=Show.objects.all()
    peoples=People.objects.all()
    reviews=Review.objects.all()
    ctx = {
        'shows' : shows,
        'peoples' : peoples,
        'reviews' : reviews,
    }
    return render(request, 'kover/show_detail.html',ctx)