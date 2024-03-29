from django.shortcuts import render, HttpResponse
from django.db.models import Count

from .models import FAQ, Category

# Create your views here.

def faq(request):
    context = {
        'faqs_of_cat': [
            {
                'category': cat,
                'faqs': FAQ.objects.filter(category=cat)
            }
            for cat in Category.objects.annotate(num_faqs=Count('faqs')).filter(num_faqs__gt=0)
        ]
    }
    return render(request, 'faq/faq.html', context)

