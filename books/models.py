from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
import os

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    year_of_publication = models.PositiveIntegerField()
    publisher = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='books'
    )
    authors = models.ManyToManyField(Author, related_name='books')
    image_cover = models.ImageField(upload_to='book_covers/')

    # view counts
    daily_views = models.PositiveIntegerField(default=0)
    monthly_views = models.PositiveIntegerField(default=0)
    yearly_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_cover:
            # full filesystem path to the saved image
            img_path = self.image_cover.path

            try:
                img = Image.open(img_path)
                target_size = (150, 230)  # width, height in pixels

                # Perform the resize (you can switch LANCZOS for ANTIALIAS in older Pillow)
                img = img.resize(target_size, Image.LANCZOS)

                # Overwrite the original file—same format, same path
                img.save(img_path)

            except Exception as e:
                # optional: log this
                print(f"Error resizing image {img_path}: {e}")

class BookCopy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    copy_code = models.CharField(
        max_length=30,
        unique=True,
        help_text="Unique inventory code or barcode for this copy."
    )
    # status fields
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} ({self.copy_code})"

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    book       = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating     = models.IntegerField(choices=RATING_CHOICES)
    review     = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('book', 'user')  # one review per user per book

    def __str__(self):
        return f"{self.user.username} → {self.book.title} ({self.rating}/5)"

    class Meta:
        unique_together = ('user', 'book')  # one review per user/book
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.book.title} — {self.rating}⭐ by {self.user.username}"

class ReviewLike(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    is_like    = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')