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
    def get(self, request, slug):
        multimedia  = model.Multimedia.objects.filter(slug = slug)
        if not multimedia.exists():
            return HttpResponseNotFound
        else:
            multimedia = list(multimedia)[0]
        title       = str(multimedia.title)
        tags        = list(multimedia.tag.all())
        images      = list(multimedia.images.all())
        videos      = list(multimedia.videos.all())
        date_created= str(multimedia.date)
        images      = [{
            "title" : str(img.title),
            "src"   : str(img.file.url),
            "date"  : str(img.date),
            "alt"   : str(img.alt)    
        } for img in images]
        videos      = [{
            "title" : str(vid.title),
            "src"   : str(vid.file.url),
            "date"  : str(vid.date),
        } for vid in videos]
        tags        = [str(tag) for tag in tags]
        context     = {
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
            title   = media.title
            tags    = media.tags.all()
            date    = media.date
            preview = media.previews.file.url
            mediaList.append({
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