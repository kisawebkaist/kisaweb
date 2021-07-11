from django.core.paginator import Paginator

from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Post, PostTag

RESULTS_PER_PAGE = 12

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
