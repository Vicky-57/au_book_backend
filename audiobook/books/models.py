from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from .middleware import get_current_user

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='books_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='books_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Role(models.Model):
    role_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.modified_by = get_current_user().username if get_current_user() else 'system'
        super().save(*args, **kwargs)

class Book(models.Model):
    book_number = models.PositiveIntegerField(unique=True)
    book_name = models.CharField(max_length=200)
    book_image = models.ImageField(upload_to='book_images/', blank=True, null=True)  # Relative path to the image
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        # Validate book_number to ensure it's non-negative
        if self.book_number < 0:
            raise ValidationError({'book_number': 'Book number cannot be negative.'})

    def save(self, *args, **kwargs):
        # Clean method is called before save
        self.clean()

        # Get the current user and set modified_by
        current_user = get_current_user()
        self.modified_by = current_user.username if current_user else 'system'

        # Call the superclass's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.book_name

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.PositiveIntegerField()  # Ensure non-negative
    chapter_name = models.CharField(max_length=200)
    chapter_image = models.ImageField(upload_to='chapter_images/', blank=True, null=True)  # Relative path to the image
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('book', 'chapter_number')  # Ensure unique chapter number within a book

    def clean(self):
        if self.chapter_number < 0:
            raise ValidationError({'chapter_number': 'Chapter number cannot be negative.'})

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        self.modified_by = get_current_user().username if get_current_user() else 'system'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.chapter_number}. {self.chapter_name}"

class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='sections')
    section_number = models.PositiveIntegerField()  # Ensure non-negative
    section_name = models.CharField(max_length=200)
    section_image = models.ImageField(upload_to='section_images/', blank=True, null=True)  # Relative path to the image
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('chapter', 'section_number')  # Ensure unique section number within a chapter

    def clean(self):
        if self.section_number < 0:
            raise ValidationError({'section_number': 'Section number cannot be negative.'})

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        self.modified_by = get_current_user().username if get_current_user() else 'system'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.section_number}. {self.section_name}"

class AudioFile(models.Model):
    file = models.FileField(upload_to='audio/')
    text_file = models.FileField(upload_to='text_files/', null=True, blank=True)

    def __str__(self):
        return self.file.name

class Shloka(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='shlokas', blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='shlokas', blank=True, null=True)
    shloka_number = models.PositiveIntegerField(null=True, blank=True)
    shlok_text = models.TextField()
    audio = models.ForeignKey(AudioFile, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.modified_by = get_current_user().username if get_current_user() else 'system'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shlok_text