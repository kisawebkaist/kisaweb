# from django.shortcuts import render, get_object_or_404
# from .models import PostCategory, Post
# from django.http import HttpResponse, HttpResponseRedirect
# from django.views.decorators.http import require_http_methods
# from django.views.generic import CreateView, UpdateView
# from .forms import PostForm, PostCategoryForm
# from django.urls import reverse
# from django import forms
# from crispy_forms.layout import HTML, Hidden
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Post, PostTag

RESULTS_PER_PAGE = 16

def post_view(request, post_slug):
  blog_post = Post.objects.filter(slug=post_slug).first()
  if blog_post == None:
    return HttpResponse('Blog Post Does Not Exist', status=404)
  context = {
    'content': blog_post.content,
    'title': blog_post.title,
    'tags': blog_post.tags,
    'image': blog_post.image,
    'created': blog_post.created,
  }
  return render(request, 'blog/blog_post.html', context)

def blog_view(request):
  searched_tags = request.GET.get('tags', '').split(',')
  posts = Post.objects.order_by('-created').all()
  if searched_tags != ['']:

    posts = Post.objects.filter(tags__tag_name__in=searched_tags).annotate(num_tags=Count('tags')).filter(num_tags=len(searched_tags)).order_by('-created')
    # print(searched_tags)
    # print(posts)

  # Pagination from previous implementation
  paginator = Paginator(posts, RESULTS_PER_PAGE)
  page_number = request.GET.get('page')

  if page_number == None:
    page_number = '1'

  page_obj = paginator.get_page(page_number)
  page_number = page_obj.number

  cnt_page_links = 5
  page_ids_l, page_ids_r = list(), list()
  add, sub = 1, 1
  for i in range(cnt_page_links):
    if page_number + add <= paginator.num_pages:
      page_ids_r.append(page_number + add)
      add += add
  for i in range(cnt_page_links):
    if page_number - sub >= 1:
      page_ids_l.append(page_number - sub)
      sub += sub
  page_ids = page_ids_l[::-1] + [page_number] + page_ids_r

  context = {
    'tagObjects': PostTag.objects.order_by('tag_name').all(),
    'posts': page_obj,
    'num_results': len(posts),
    'page_ids': page_ids,
    'cur_page': page_number
  }
  return render(request, 'blog/blog_posts.html', context)

# '''
#   The functions below are used for creating the HTML format for the
#   recursively defined dropdown menus and elements of the category
#   nav-bar. 
# '''

# # BLOG NAVBAR - RECURSIVE DROPDOWN => BEGIN

# def html_element(tag, content, attrs):
#   attrs = ' '.join([f'{attr[0]}="{attr[1]}"' for attr in attrs.items()])
#   return f'<{tag} {attrs}>{content}</{tag}>'

# def construct_category_children():
#   category_children = {}
#   for category in PostCategory.objects.all():
#     parent_category = category.parent_category
#     if parent_category != None:
#       if not parent_category in category_children:
#         category_children[parent_category] = []
#       category_children[parent_category].append(category)
#   return category_children

# def get_dropdown_menu(category, category_children):
#   tag = 'div'
#   attrs = {
#     'class': 'dropdown-menu bg-light',
#   }
#   content = ''
#   for child in category_children[category]:
#     content += new_dropdown_item(child, category_children)
#   return html_element(tag, content, attrs)

# def get_dropdown_buttons(category):
#   result = ''

#   tag = 'a'
#   attrs = {
#     'type': 'button',
#     'class': 'btn btn-sm btn-light',
#     'style': 'border-right:0px',
#   }
#   content = category.name
#   attrs['href'] = category.get_absolute_url()

#   result += html_element(tag, content, attrs)

#   del attrs['style']
#   del attrs['href']
#   attrs['class'] += ' dropdown-toggle dropdown-toggle-split my-toggler' # delete unnecessary items
#   attrs['aria-haspopup'] = 'true'
#   attrs['aria-expanded'] = 'false'
#   content = ''

#   result += html_element(tag, content, attrs)

#   return result


# def new_dropdown(category, category_children, attrs):
#   tag = 'div'
#   if not 'class' in attrs:
#     attrs['class'] = 'btn-group'
#   else:
#     attrs['class'] += ' btn-group'

#   content = ''
#   content += get_dropdown_buttons(category)
#   content += get_dropdown_menu(category, category_children)

#   return html_element(tag, content, attrs)

# def new_item(category, category_children, attrs):

#   if category in category_children:
#     return new_dropdown(category, category_children, attrs)
  
#   attrs['type'] = 'button'
#   if not 'class' in attrs:
#     attrs['class'] = 'btn btn-sm btn-light'
#   else:
#     attrs['class'] += ' btn btn-sm btn-light'
#   attrs['href'] = category.get_absolute_url()
  
#   tag = 'a'
#   content = category.name

#   return html_element(tag, content, attrs)

# def new_dropdown_item(category, category_children):
#   tag = 'div'
#   attrs = {
#     'class': 'row justify-content-center',
#   }
#   content = new_item(category, category_children, {})

#   return html_element(tag, content, attrs)

# def new_nav_item(category, category_children):
#   attrs = {
#     'class': 'nav-item',
#   }

#   return new_item(category, category_children, attrs)
  
# def create_blog_navbar(context):
#   category_children = construct_category_children()
#   blog_navbar = ''
#   for category in PostCategory.objects.all():
#     parent_category = category.parent_category
#     if parent_category == None:
#       blog_navbar = blog_navbar + new_nav_item(category, category_children)
#   context['blog_navbar'] = blog_navbar

# # BLOG NAVBAR - RECURSIVE DROPDOWN => END



# # Create your views here.


# def post_view(request, category_slug, post_slug):
#   category_object = PostCategory.objects.filter(slug=category_slug).first()
#   if category_object == None:
#     return HttpResponse('Category Does Not Exist', status=404)
  
#   post_object = Post.objects.filter(category=category_object, slug=post_slug).first()
#   if post_object == None:
#     return HttpResponse('Post Does Not Exist', status=404)

#   context = {
#     'category': category_object,
#     'post_slug': post_slug,
#     'post': post_object,
#     'user_can_change': request.user.has_perm('blog.change_post'),
#   }
#   create_blog_navbar(context)

#   return render(request, 'blog/blog_post.html', context)

# def category_view(request, category_slug):
  
#   '''
#     This means: Get the category objects with either belonging to this category
#     or belonging to one of the sub-categories.
#   '''
#   category_objects = PostCategory.objects.filter(slug__regex=rf'^({category_slug}|{category_slug}-_sub_-.+)$').all()
#   if category_objects == None:
#     return HttpResponse('Category Does Not Exist', status=404)

#   posts = Post.objects.filter(category__in=category_objects).order_by('-created').all()
#   paginator = Paginator(posts, 3)
#   page_number = request.GET.get('page')

#   if page_number == None:
#     page_number = '1'

#   page_obj = paginator.get_page(page_number)
#   page_number = page_obj.number

#   cnt_page_links = 5
#   page_ids_l, page_ids_r = list(), list()
#   add, sub = 1, 1
#   for i in range(cnt_page_links):
#     if page_number + add <= paginator.num_pages:
#       page_ids_r.append(page_number + add)
#       add += add
#   for i in range(cnt_page_links):
#     if page_number - sub >= 1:
#       page_ids_l.append(page_number - sub)
#       sub += sub
#   page_ids = page_ids_l[::-1] + [page_number] + page_ids_r

#   context = {
#     'category': category_objects.first(),
#     'posts': page_obj,
#     'page_ids': page_ids,
#     'cur_page': page_number,
#     'user_can_change': request.user.has_perm('blog.change_post'),
#   } 
#   create_blog_navbar(context)
  
#   return render(request, 'blog/blog_posts.html', context)

# def blog_view(request):

#   posts = Post.objects.order_by('-created').all()

#   paginator = Paginator(posts, 3)
#   page_number = request.GET.get('page')

#   if page_number == None:
#     page_number = '1'

#   page_obj = paginator.get_page(page_number)
#   page_number = page_obj.number

#   cnt_page_links = 5
#   page_ids_l, page_ids_r = list(), list()
#   add, sub = 1, 1
#   for i in range(cnt_page_links):
#     if page_number + add <= paginator.num_pages:
#       page_ids_r.append(page_number + add)
#       add += add
#   for i in range(cnt_page_links):
#     if page_number - sub >= 1:
#       page_ids_l.append(page_number - sub)
#       sub += sub
#   page_ids = page_ids_l[::-1] + [page_number] + page_ids_r

#   context = {
#     'posts': page_obj,
#     'page_ids': page_ids,
#     'cur_page': page_number,
#     'user_can_change': request.user.has_perm('blog.change_post'),
#   }
#   create_blog_navbar(context)
  
#   return render(request, 'blog/blog_posts.html', context)

# '''
#   This is the view for creating a new category
# '''

# class PostCategoryCreate(CreateView):
#   model = PostCategory
#   form_class = PostCategoryForm

#   '''
#     Intervening the GET method to inject the permission
#     requirements of the user.
#   '''
#   def get(self, *args, **kwargs):
#     if not self.request.user.has_perm('blog.add_post_category'):
#       return HttpResponse('You are not allowed to access this page', 403)
#     return super().get(self, *args, **kwargs)

#   '''
#     Intervening the POST method to check whether the user
#     has the permission to send a POST request, and to check whether
#     the user cancels the post creation.
#   '''
#   def post(self, request, *args, **kwargs):
#     if not self.request.user.has_perm('blog.add_post_category'):
#       return HttpResponse('You are not allowed to access this page', 403)
    
#     if 'cancel' in request.POST:
#       return HttpResponseRedirect(reverse('blog'))
    
#     return super().post(request, *args, **kwargs)  

# '''
#   This is the view for creating a new post
# '''
# class PostCreate(CreateView):
#   model = Post
#   form_class = PostForm

#   '''
#     Intervening the GET method to inject the permission
#     requirements of the user.
#   '''
#   def get(self, *args, **kwargs):
#     if not self.request.user.has_perm('blog.add_post'):
#       return HttpResponse('You are not allowed to access this page', 403)
#     return super().get(self, *args, **kwargs)

#   '''
#     Intervening the get_form function to hide the 'author'
#     field from the user and automatically assign the current
#     user as the author.
#   '''
#   def get_form(self, form_class=None):
#     form = super().get_form(form_class)
#     #form.fields['author'].widget = forms.HiddenInput()
#     #form.fields['author'].initial = self.request.user
#     return form

#   '''
#     Intervening the POST method to check whether the user
#     has the permission to send a POST request, and to check whether
#     the user cancels the post creation.
#   '''
#   def post(self, request, *args, **kwargs):
#     if not self.request.user.has_perm('blog.add_post'):
#       return HttpResponse('You are not allowed to access this page', 403)
    
#     if 'cancel' in request.POST:
#       return HttpResponseRedirect(reverse('blog'))
    
#     return super().post(request, *args, **kwargs)

# class PostUpdate(UpdateView):
#   model = Post
#   form_class = PostForm

#   '''
#     Overriding the get_object function since it checks only for one slug/pk field
#     but we have two of them for a post (category slug and post slug).
#     By retrieving those information from the uri, we either return 404 or obtain the 
#     Post object.
#   '''
#   def get_object(self):
#     uri = self.request.build_absolute_uri()[:-1].split('/')
#     return get_object_or_404(self.model, slug=uri[-1], category=PostCategory.objects.filter(slug=uri[-2]).first())

#     '''
#     Intervening the get_form function to hide the 'author'
#     field from the user. Moreover, since the UpdateView should 
#     have a delete button as well, we add a delete button 
#     to the PostForm class defined in the forms.py file. 

#   '''

#   def get_form(self, form_class=None):
#     form = super().get_form(form_class)
#     #form.fields['author'].widget = forms.HiddenInput()

#     uri = self.request.build_absolute_uri()[:-1].split('/')
#     cancel_url = reverse('post', kwargs={'category_slug': uri[-2], 'post_slug': uri[-1]})
    
#     form.helper.layout[-1][0].append(HTML(
#       f'<button name="delete" class="btn btn-danger" data-slug="{uri[-2]}/{uri[-1]}" data-post-delete-url="{{% url "delete" category_slug="{uri[-2]}" post_slug="{uri[-1]}" %}}" id="post_delete">Delete</button>'
#     ))

#     form.helper.layout.append(Hidden(
#       'next',
#       '{% if request.META.HTTP_REFERER %}{{ request.META.HTTP_REFERER }}{% else %}' + cancel_url + '{% endif %}'
#     ))

#     return form

#   '''
#     Intervening the GET method to inject the permission
#     requirements of the user.
#   '''
#   def get(self, *args, **kwargs):
#     if not self.request.user.has_perm('blog.change_post'):
#       return HttpResponse('You are not allowed to access this page', 403)
#     return super().get(self, *args, **kwargs)

#   '''
#     Intervening the POST method to check whether the user
#     has the permission to send a POST request, and to check whether
#     the user cancels the post update.
#   '''
#   def post(self, request, *args, **kwargs):
#     if not self.request.user.has_perm('blog.change_post'):
#       return HttpResponse('You are not allowed to access this page', 403)
    
#     if 'cancel' in request.POST:
#       uri = self.request.build_absolute_uri()[:-1].split('/')
#       cancel_url = reverse('post', kwargs={'category_slug': uri[-2], 'post_slug': uri[-1]})
#       return HttpResponseRedirect(request.POST.get('next', cancel_url))  
    
#     return super().post(request, *args, **kwargs)

# '''
#   Decorators for indicating the facts that:
#     1) The user must be logged in
#     2) Only POST requests are accepted
# '''
# @login_required
# @require_http_methods(['POST'])
# def delete_post(request, category_slug, post_slug):
#   category = PostCategory.objects.filter(slug=category_slug).first()
#   post = Post.objects.filter(category=category, slug=post_slug).first()
  
#   post.delete()
#   return HttpResponse(reverse('blog'))