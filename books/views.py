# Create your views here.
from django.shortcuts import render,get_object_or_404, redirect
from django.core.paginator import  Paginator
from django.utils import timezone
from django.db.models import Q, Count
from django.db.models import Avg
from .models import Book, Author, Category, Review, ReviewLike
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home_view(request):
    featured = Book.objects.order_by('-monthly_views')[:4]
    popular  = Book.objects.order_by('-yearly_views')[:8]
    recently = Book.objects.order_by('-pk')[:5]
    from .models import Category
    categories = Category.objects.all()

    return render(request, 'books/home.html', {
        'recent_books': recently,
        'featured_books': featured,
        'popular_books': popular,
        'categories': categories,
    })


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books    = Book.objects.filter(categories=category).distinct()
    return render(request, 'books/category_list.html', {
        'category': category,
        'books':     books,
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # increment view-counts (simple example)
    now = timezone.now()
    book.daily_views   += 1
    book.monthly_views += 1
    book.yearly_views  += 1
    book.save(update_fields=['daily_views','monthly_views','yearly_views'])

    reviews = (
        Review.objects
        .filter(book=book)
        .annotate(
            likes_count=Count('likes', filter=Q(likes__is_like=True)),
            dislikes_count=Count('likes', filter=Q(likes__is_like=False))
        )
        .order_by('-likes_count', '-created_at')
    )

    # Average rating
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']

    # Review form
    form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Update or create so we never violate the unique constraint
            rev, created = Review.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'review': form.cleaned_data['review']
                }
            )
            return redirect('books:detail', pk=book.pk)

    # Range helper for stars
    rating_range = range(1, 6)

    # Check if current user liked/disliked each review
    user_likes = {}
    if request.user.is_authenticated:
        likes = ReviewLike.objects.filter(user=request.user, review__in=reviews)
        user_likes = {like.review_id: like.is_like for like in likes}

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'rating_range': rating_range,
        'user_likes': user_likes,
    })
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books  = author.books.all()
    return render(request, 'books/author_detail.html', {
        'author': author,
        'books':  books,
    })

def book_list(request):
    qs = Book.objects.all()

    # Search by title or author name
    q = request.GET.get('q')
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(authors__name__icontains=q)
        )

    # Filter by category slug
    cat = request.GET.get('category')
    if cat:
        qs = qs.filter(categories__slug=cat)

    # Filter by language
    lang = request.GET.get('language')
    if lang:
        qs = qs.filter(language__iexact=lang)

    # Filter by publication year
    yr = request.GET.get('year')
    if yr and yr.isdigit():
        qs = qs.filter(year_of_publication=int(yr))

    # Remove duplicates (due to M2M joins), then paginate
    qs = qs.distinct().order_by('title')
    paginator = Paginator(qs, 20)            # 20 books per page
    page_obj  = paginator.get_page(request.GET.get('page'))

    # For filter dropdowns
    categories = Category.objects.all()
    languages  = Book.objects.values_list('language', flat=True).distinct()
    years      = Book.objects.values_list('year_of_publication', flat=True).distinct()

    return render(request, 'books/list.html', {
        'page_obj':   page_obj,
        'categories': categories,
        'languages':  languages,
        'years':      sorted(years, reverse=True),
        'q':          q or '',
        'selected_category': cat or '',
        'selected_language': lang or '',
        'selected_year':     yr or '',
    })



@login_required
def review_like(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    # toggle or create
    obj, created = ReviewLike.objects.update_or_create(
        user= request.user,
        review= review,
        defaults={'is_like': True}
    )
    # If they had previously disliked, this flips it
    return redirect('books:detail', pk=review.book.pk)

@login_required
def review_dislike(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    obj, created = ReviewLike.objects.update_or_create(
        user= request.user,
        review= review,
        defaults={'is_like': False}
    )
    return redirect('books:detail', pk=review.book.pk)
