from django.shortcuts import render, HttpResponse

from .models import Question

# Create your views here.

def faq(request):
    context = {
        'faq_list': Question.objects.filter(faq=True)
    }
    return render(request, 'faq/faq.html', context)

def cat(request):
    context = {
        'cat_list': Category.objects.filter()
    }
    return render(request, 'faq/faq.html', context)
