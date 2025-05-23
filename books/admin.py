# books/admin.py
from django.contrib import admin
from .models import Author, Category, Book, BookCopy, Review

class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1
    readonly_fields = ('id', 'added_on')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'isbn',
        'publisher',
        'year_of_publication',
        'language',
        'display_categories'

    )
    list_filter = (
        'categories',
        'language',
        'year_of_publication',
    )
    search_fields = (
        'title',
        'isbn',
        'authors__name',
    )
    filter_horizontal = ('authors','categories')
    readonly_fields = (
        'daily_views',         # updated
        'monthly_views',       # updated
        'yearly_views',        # updated
    )
    inlines = [BookCopyInline]

    @admin.display(description='Categories')
    def display_categories(self, obj):
        return ", ".join(cat.name for cat in obj.categories.all())

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('copy_code', 'book', 'is_available', 'added_on')
    list_filter = ('is_available', 'book')
    search_fields = ('copy_code', 'book__title')
    raw_id_fields = ('book',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('book','user','rating','created_at')
    list_filter   = ('rating','created_at')
    search_fields = ('book__title','user__username','review')

