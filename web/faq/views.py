from django.shortcuts import render, HttpResponse

from .models import FAQ, Category

# Create your views here.

def faq(request):
    context = {
        'faqs_of_cat': [
            {
                'category': cat,
                'faqs': FAQ.objects.filter(category=cat)
            }
            for cat in Category.objects.all()
        ]
    }
    return render(request, 'faq/faq.html', context)

