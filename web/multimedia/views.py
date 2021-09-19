from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, Http404
import multimedia.models as model


RESULTS_PER_PAGE = 5


class Video(View):
    def get(self, request, slug):
        video   = model.Video.objects.filter(slug = slug)
        if video.exists():
            video       = list(video)[0]
            videoFile   = video.file.url
            return redirect(videoFile)
        else:
            return HttpResponseNotFound


class Image(View):
    def get(self, request, slug):
        image   = model.Image.objects.filter(slug = slug)
        if image.exists():
            image       = list(image)[0]
            imageFile   = image.file.url
            return redirect(imageFile)
        else:
            return HttpResponseNotFound


class MultimediaView(View):
    def get(self, request, pk):
        multimedia  = model.Multimedia.objects.filter(pk=pk)[0]
        if not multimedia:
            return HttpResponseNotFound
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
        multimedia = model.Multimedia.objects.all().order_by('date', 'title')

        if tag_data != ['']:
            multimedia = multimedia.filter(tags__tag_name__in=tag_data).annotate(num_tags=Count('tags')).filter(num_tags=len(tag_data))
        print(multimedia)

        # TODO: PAGINATION
        multimedia  = multimedia[:RESULTS_PER_PAGE]

        mediaList   = []
        for media in multimedia:
            pk      = media.id
            title   = media.title
            tags    = media.tags.all()
            date    = media.date
            preview = media.previews.file.url
            mediaList.append({
                "id"     : pk,
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


# class TagFilter(View):
#     #this is to render the tag filtering thing
#     def get(self, request, slug):
#         #searching
#         tag_data    = slug.get('tags', '').split(',')
#         render_data = model.Multimedia.objects.filter(tag__tag_name___in = tag_data).distinct()
#         context = {
#             'tagObjects': model.MultimediaTags.objects.all(),
#             'render'    : render_data
#         }
#         return render(request, 'multimedia/search.html', context = context)


#02-02-2002_videoTitle.mp4
#videoTitle -> 02-02-2002_videoTitle.mp4
#/multimediaName/vid/videoTitle.mp4
#/multimediaName/img/imageTitle.jpeg