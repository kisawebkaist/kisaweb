from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone, dateformat
from election.expression_parser import evaluate

from .models import Image


@login_required
def index(request):
    '''
    This view will render the index.html template which will have the form to upload the image
    '''
    return render(request, 'image_uploader/image_uploader.html')

@login_required
def upload(request):
    '''
    This view will handle the image upload and save the image information in the database
    '''
    if request.method == 'POST':
        title = request.POST.get('title')
        alt = request.POST.get('alt')
        file = request.FILES.get('file')
        user = request.user
        
        # Get the current date
        date = timezone.now()

        # Validate form data (optional)
        if not (title and alt and date and file):
            messages.error(request, 'Please fill in all required fields')
            return redirect(reverse('image_uploader'))
        
        # Create Image object and save to database
        image = Image(title=title, alt=alt, date=date, user=user, file=file)

        image.save()

        messages.success(request, 'Image uploaded successfully')
        return redirect(reverse('view_images'))
    else:
        return redirect(reverse('image_uploader'))



@login_required
def view_images(request):
    '''
    This view will render the view_images.html template which will display the images uploaded by the user
    '''
    images = Image.objects.filter(user=request.user)
    return render(request, 'image_uploader/view_images.html', {'images': images})
