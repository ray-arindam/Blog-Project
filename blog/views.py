from django.db.models import Count,Q
from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect
from .models import Post,Category,Author,PostView
from marketing.models import Signup
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import CommentForm,PostForm
from django.urls import reverse
from django.contrib.auth import get_user

# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | 
            Q(overview__icontains=query) 
        )
    context = {'queryset':queryset}

    return render(request,'search.html',context = context)

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method == "POST":
        email = request.POST['email']
        new_signup = Signup(email=email)
        new_signup.save()

    context = {
        'object_list':featured,
        'latest':latest
    }
    return render(request,'index.html',context=context)

def blog(request):
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    category_count = get_category_count()
    post_list = Post.objects.all()
    paginator = Paginator(post_list,2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'post_list':paginated_queryset,
        'page_request_var':page_request_var,
        'most_recent':most_recent,
        'category_count':category_count

    }
    return render(request,'blog.html',context=context)

def post(request,id):
    latest_posts = Post.objects.order_by('-timestamp')[0:3]
    category_count = get_category_count()   
    post = get_object_or_404(Post,id=id)

    PostView.objects.get_or_create(user=request.user,post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user.author
            form.instance.post = post
            form.save()
            return redirect(reverse("blog:post-detail",kwargs={
                'id':post.id
            }))

    context = {
        'post':post,
        'most_recent':latest_posts,
        'category_count':category_count,
        'comment_form':form,
        }
    return render(request,'post.html',context=context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None,request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(form.instance.get_absolute_url())
    context = {
        "form":form,
        'title':title,
    }
    return render(request,'post_create.html',context=context)

def post_update(request,id):
    title ='Update'
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(form.instance.get_absolute_url())
    context = {
        "form":form,
        'title':title,
    }
    return render(request,'post_create.html',context=context)

def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    return redirect(reverse('blog:blog'))
