import django_filters
from .models import Book, Chapter, Section

class BookFilterSet(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['book_number', 'book_name']  # Adjust according to your model fields

class ChapterFilterSet(django_filters.FilterSet):
    class Meta:
        model = Chapter
        fields = ['chapter_number', 'chapter_name', 'book']  # Adjust according to your model fields

class SectionFilterSet(django_filters.FilterSet):
    class Meta:
        model = Section
        fields = ['section_number', 'section_name', 'chapter']  # Adjust according to your model fields
