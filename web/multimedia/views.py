from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django.db.models import Count
import multimedia.models as model


RESULTS_PER_PAGE = 5
class MultimediaView(View):
    def get(self, request, slug):
        multimedia  = model.Multimedia.objects.filter(slug = slug)
        if not multimedia.exists():
            return HttpResponseNotFound
        multimedia  = multimedia[0]
        pk           = multimedia.id
        title        = multimedia.title
        tags         = multimedia.tags.all()
        images       = multimedia.images.all()
        videos       = multimedia.videos.all()
        date_created = multimedia.date
        images       = [{
            "title" : img.title,
            "src"   : img.file.url,
            "date"  : img.date,
            "alt"   : img.alt    
        } for img in images]
        images.sort(key=lambda x: x["title"].lower())
        videos      = [{
            "title" : vid.title,
            "src"   : vid.file.url,
            "date"  : vid.date,
        } for vid in videos]
        context     = {
            "id"    : pk,
            "title" : title,
            "tags"  : tags,
            "images": images,
            "videos": videos,
            "date"  : date_created

        }
        return render(request, 'multimedia/multimedia.html', context = context)


class HomePageView(View):
    def get(self, request):
        tag_data   = self.request.GET.get('tags', '').split(',')
        multimedia = model.Multimedia.objects.filter_and(tag_data).order_by('date', 'title')

        # TODO: PAGINATION
        multimedia  = multimedia[:RESULTS_PER_PAGE]

        mediaList   = []
        for media in multimedia:
            slug    = media.slug
            title   = media.title
            tags    = media.tags.all()
            date    = media.date
            preview = media.previews.file.url
            mediaList.append({
                "slug"   : slug,
                "title"  : title,
                "tags"   : tags,
                "preview": preview,
                "date"   : date
            })
        context = {
            "multimedia": mediaList,
            'tagObjects': model.MultimediaTag.objects.all(),
        }
        return render(request, "multimedia/multimedia_home.html", context = context)


#02-02-2002_videoTitle.mp4
#videoTitle -> 02-02-2002_videoTitle.mp4
#/multimediaName/vid/videoTitle.mp4
#/multimediaName/img/imageTitle.jpeg