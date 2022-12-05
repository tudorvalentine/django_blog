from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from .forms import CommentForm

def post_list(request):
    object_list = Post.objects.all()

    paginator = Paginator(object_list , 3)
    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts.paginator.get_page(1)
    except EmptyPage:
        posts.paginator.get_page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page' : page, 'posts' : posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    form_comment = None
    # Daca forma a fost trimisa
    if request.method ==  'POST':
        # Construim formularul cu date primite prin metoda POST
        form_comment = CommentForm(request.POST)
        # Daca formularul a trecut validarea
        if form_comment.is_valid():
            # creem comentariul fără a salva pentru a asocia comentariul cu postarea curenta
            new_comment = form_comment.save(commit=False)
            # asociem comentariul cu postare
            new_comment.post = post
            # salvam comentariul in baza de date
            new_comment.save()
    else:
        form_comment = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments' : comments, 'new_comment' : new_comment, 'form_comment' : form_comment})


