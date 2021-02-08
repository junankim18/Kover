from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

def profile_block(request):
    show = Show.objects.all()
    user = Profile.objects.get(id=request.user.pk)
    pk = user.pk
    ctx = {
        'show': show
    }
    return render(request, 'kover/profile_block.html', ctx)




class Feed(View):
    template_name = 'kover/feed_layout.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Feed, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        feed_list = Feed_post.objects.all()
        ctx = {"feeds": feed_list}
        return render(request, self.template_name, ctx)

    def post(self, request):
        request = json.loads(request.body)
        feed_id = request['id']
        button_type = request['type']
        feed = Feed_post.objects.get(id=feed_id)
        comment = Feed_comment.objects.get(id=feed_id)
        if button_type == feed_like:
            feed_like = feed_like + 1
        Feed_post.save()

        return JsonResponse({'id': feed_id, 'type':feed_like})


