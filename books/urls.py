from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('',                     views.home_view,      name='home'),
    path('list/',                views.book_list,      name='list'),
    path('book/<int:pk>/',       views.book_detail,    name='detail'),
    path('author/<int:pk>/',     views.author_detail,  name='author-detail'),
    path('category/<slug:slug>/',views.category_list,  name='category-list'),
    path('review/<int:review_id>/like/',    views.review_like,    name='review-like'),
    path('review/<int:review_id>/dislike/', views.review_dislike, name='review-dislike'),
]