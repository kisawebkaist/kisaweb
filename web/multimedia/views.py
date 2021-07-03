from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse, Http404
import multimedia.models as model
class Video(View):
    def get(self, request, slug):
        video   = model.Video.objects.filter(slug = slug)
        if video.exists():
            video       = list(video)[0]
            videoFile   = video.file.url
            return redirect(videoFile)
        else:
            return Http404
    
class Image(View):
    def get(self, request, slug):
        image   = model.Image.objects.filter(slug = slug)
        if image.exists():
            image       = list(image)[0]
            imageFile   = image.file.url
            return redirect(imageFile)
        else:
            return Http404

class Multimedia(View):
    def get(self, request, slug):
        multimedia  = model.Multimedia.objects.filter(slug = slug)
        if multimedia.exists():
            multimedia = list(multimedia)[0]
            image   = multimedia.images.all()
            video   = multimedia.videos.all()
            imgDict = [{'title' : img.title, 'alt' : img.alt, 'slug' : img.slug, 'src' : img.file.url} for img in image]
            vidDict = [{'title' : vid.title, 'slug': vid.slug, 'src' : vid.file.url} for vid in video]
            respDic = {
                'image' : imgDict,
                'video' : vidDict
            }
            return render(request, 'html/multimedia.html', context = respDic)
        else:
            return Http404

class HomePage(View):
    #this is to render the home page
    def get(self, request):
        #get top 5 most recent
        multimedia  = model.Multimedia.objects.all()
        tag         = model.MultimediaTags.objects.all()
        context     = {
            "multimedia" : multimedia, 
            "tagData"     : tag
        }
        return render(request, 'html/home.html', context = context)
    
class TagFilter(View):
    #this is to render the tag filtering thing
    def get(self, request, slug):
        #searching
        tag_data    = slug.get('tags', '').split(',')
        render_data = Multimedia.objects.filter(tag__tag_name___in = tag_data).distinct()
        context = {
            'tagObjects' : model.MultimediaTags.objects.all(),
            'render'     : render_data
        }
        return render(request, 'html/search.html', context = context)

#02-02-2002_videoTitle.mp4
#videoTitle -> 02-02-2002_videoTitle.mp4
#/multimediaName/vid/videoTitle.mp4
#/multimediaName/img/imageTitle.jpeg