from django.shortcuts import render, get_object_or_404
from .models import PostCategory, Post
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView
from .forms import PostForm
from django.urls import reverse
from django import forms
from crispy_forms.layout import HTML, Hidden
from django.contrib.auth.decorators import login_required

'''
  The functions below are used for creating the HTML format for the
  recursively defined dropdown menus and elements of the category
  nav-bar. 
'''

# BLOG NAVBAR - RECURSIVE DROPDOWN => BEGIN

def html_element(tag, content, attrs):
  attrs = ' '.join([f'{attr[0]}="{attr[1]}"' for attr in attrs.items()])
  return f'<{tag} {attrs}>{content}</{tag}>'

def construct_category_children():
  category_children = {}
  for category in PostCategory.objects.all():
    parent_category = category.parent_category
    if parent_category != None:
      if not parent_category in category_children:
        category_children[parent_category] = []
      category_children[parent_category].append(category)
  return category_children

def get_dropdown_menu(category, category_children):
  tag = 'div'
  attrs = {
    'class': 'dropdown-menu bg-light',
  }
  content = ''
  for child in category_children[category]:
    content += new_dropdown_item(child, category_children)
  return html_element(tag, content, attrs)

def get_dropdown_buttons(category):
  result = ''

  tag = 'a'
  attrs = {
    'type': 'button',
    'class': 'btn btn-sm btn-light',
    'style': 'border-right:0px',
  }
  content = category.name
  attrs['href'] = category.get_absolute_url()

  result += html_element(tag, content, attrs)

  del attrs['style']
  del attrs['href']
  attrs['class'] += ' dropdown-toggle dropdown-toggle-split my-toggler' # delete unnecessary items
  attrs['aria-haspopup'] = 'true'
  attrs['aria-expanded'] = 'false'
  content = ''

  result += html_element(tag, content, attrs)

  return result


def new_dropdown(category, category_children, attrs):
  tag = 'div'
  if not 'class' in attrs:
    attrs['class'] = 'btn-group'
  else:
    attrs['class'] += ' btn-group'

  content = ''
  content += get_dropdown_buttons(category)
  content += get_dropdown_menu(category, category_children)

  return html_element(tag, content, attrs)

def new_item(category, category_children, attrs):

  if category in category_children:
    return new_dropdown(category, category_children, attrs)
  
  attrs['type'] = 'button'
  if not 'class' in attrs:
    attrs['class'] = 'btn btn-sm btn-light'
  else:
    attrs['class'] += ' btn btn-sm btn-light'
  attrs['href'] = category.get_absolute_url()
  
  tag = 'a'
  content = category.name

  return html_element(tag, content, attrs)

def new_dropdown_item(category, category_children):
  tag = 'div'
  attrs = {
    'class': 'row justify-content-center',
  }
  content = new_item(category, category_children, {})

  return html_element(tag, content, attrs)

def new_nav_item(category, category_children):
  attrs = {
    'class': 'nav-item',
  }

  return new_item(category, category_children, attrs)
  
def create_blog_navbar(context):
  category_children = construct_category_children()
  blog_navbar = ''
  for category in PostCategory.objects.all():
    parent_category = category.parent_category
    if parent_category == None:
      blog_navbar = blog_navbar + new_nav_item(category, category_children)
  context['blog_navbar'] = blog_navbar

# BLOG NAVBAR - RECURSIVE DROPDOWN => END



# Create your views here.

def post_view(request, category_slug, post_slug):
  category_object = PostCategory.objects.filter(slug=category_slug).first()
  if category_object == None:
    return HttpResponse('Category Does Not Exist', status=404)
  
  post_object = Post.objects.filter(category=category_object, slug=post_slug).first()
  if post_object == None:
    return HttpResponse('Post Does Not Exist', status=404)

  context = {
    'category': category_object,
    'post_slug': post_slug,
    'post': post_object,
    'user_can_change': request.user.has_perm('blog.change_post'),
  }
  create_blog_navbar(context)

  return render(request, 'blog/templates/blog/blog_post.html', context)

def category_view(request, category_slug):
  
  '''
    This means: Get the category objects with either belonging to this category
    or belonging to one of the sub-categories.
  '''
  category_objects = PostCategory.objects.filter(slug__regex=rf'^({category_slug}|{category_slug}-_sub_-.+)$').all()
  if category_objects == None:
    return HttpResponse('Category Does Not Exist', status=404)
  
  context = {
    'category': category_objects[0],
    'posts': Post.objects.filter(category__in=category_objects).order_by('-created').all(),
    'user_can_change': request.user.has_perm('blog.change_post'),
  } 
  create_blog_navbar(context)
  
  return render(request, 'blog/templates/blog/blog_posts.html', context)

def blog_view(request):
  context = {
    'posts': Post.objects.order_by('-created').all(),
    'user_can_change': request.user.has_perm('blog.change_post'),
  }
  create_blog_navbar(context)
  
  return render(request, 'blog/templates/blog/blog_posts.html', context)

'''
  This is the view for creating a new post
'''
class PostCreate(CreateView):
  model = Post
  form_class = PostForm

  '''
    Intervening the GET method to inject the permission
    requirements of the user.
  '''
  def get(self, *args, **kwargs):
    if not self.request.user.has_perm('blog.add_post'):
      return HttpResponse('You are not allowed to access this page', 403)
    return super().get(self, *args, **kwargs)

  '''
    Intervening the get_form function to hide the 'author'
    field from the user and automatically assign the current
    user as the author.
  '''
  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    form.fields['author'].widget = forms.HiddenInput()
    form.fields['author'].initial = self.request.user
    return form

  '''
    Intervening the POST method to check whether the user
    has the permission to send a POST request, and to check whether
    the user cancels the post creation.
  '''
  def post(self, request, *args, **kwargs):
    if not self.request.user.has_perm('blog.add_post'):
      return HttpResponse('You are not allowed to access this page', 403)
    
    if 'cancel' in request.POST:
      return HttpResponseRedirect(reverse('blog:blog'))
    
    return super().post(request, *args, **kwargs)

class PostUpdate(UpdateView):
  model = Post
  form_class = PostForm

  '''
    Overriding the get_object function since it checks only for one slug/pk field
    but we have two of them for a post (category slug and post slug).
    By retrieving those information from the uri, we either return 404 or obtain the 
    Post object.
  '''
  def get_object(self):
    uri = self.request.build_absolute_uri()[:-1].split('/')
    return get_object_or_404(self.model, slug=uri[-1], category=PostCategory.objects.filter(slug=uri[-2]).first())

    '''
    Intervening the get_form function to hide the 'author'
    field from the user. Moreover, since the UpdateView should 
    have a delete button as well, we add a delete button 
    to the PostForm class defined in the forms.py file. 

  '''

  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    form.fields['author'].widget = forms.HiddenInput()

    uri = self.request.build_absolute_uri()[:-1].split('/')
    cancel_url = reverse('blog:post', kwargs={'category_slug': uri[-2], 'post_slug': uri[-1]})
    
    form.helper.layout[-1][0].append(HTML(
      f'<button name="delete" class="btn btn-danger" data-slug="{uri[-2]}/{uri[-1]}" data-post-delete-url="{{% url "blog:delete" category_slug="{uri[-2]}" post_slug="{uri[-1]}" %}}" id="post_delete">Delete</button>'
    ))

    form.helper.layout.append(Hidden(
      'next',
      '{% if request.META.HTTP_REFERER %}{{ request.META.HTTP_REFERER }}{% else %}' + cancel_url + '{% endif %}'
    ))

    return form

  '''
    Intervening the GET method to inject the permission
    requirements of the user.
  '''
  def get(self, *args, **kwargs):
    if not self.request.user.has_perm('blog.change_post'):
      return HttpResponse('You are not allowed to access this page', 403)
    return super().get(self, *args, **kwargs)

  '''
    Intervening the POST method to check whether the user
    has the permission to send a POST request, and to check whether
    the user cancels the post update.
  '''
  def post(self, request, *args, **kwargs):
    if not self.request.user.has_perm('blog.change_post'):
      return HttpResponse('You are not allowed to access this page', 403)
    
    if 'cancel' in request.POST:
      uri = self.request.build_absolute_uri()[:-1].split('/')
      cancel_url = reverse('blog:post', kwargs={'category_slug': uri[-2], 'post_slug': uri[-1]})
      return HttpResponseRedirect(request.POST.get('next', cancel_url))  
    
    return super().post(request, *args, **kwargs)

'''
  Decorators for indicating the facts that:
    1) The user must be logged in
    2) Only POST requests are accepted
'''
@login_required
@require_http_methods(['POST'])
def delete_post(request, category_slug, post_slug):
  category = PostCategory.objects.filter(slug=category_slug).first()
  post = Post.objects.filter(category=category, slug=post_slug).first()
  
  post.delete()
  return HttpResponse(reverse('blog:blog'))