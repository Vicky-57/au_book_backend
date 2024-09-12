from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters 
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.exceptions import NotFound
from django.core.serializers.json import DjangoJSONEncoder
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Chapter, Section, Shloka, AudioFile
from .serializers import BookSerializer, ChapterSerializer, SectionSerializer, ShlokaSerializer, AudioFileSerializer
from .filters import BookFilterSet, ChapterFilterSet, SectionFilterSet
from books import urls as books
from django.conf import settings

def book_list(request):
    books = Book.objects.all().values(
        'id', 'book_number', 'book_name', 'book_image'
    )
    books = list(books)
    for book in books:
        if book['book_image']:
            book['book_image'] = request.build_absolute_uri(settings.MEDIA_URL + str(book['book_image']))
    return JsonResponse(books, safe=False)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    chapters = Chapter.objects.filter(book=pk).values(
        'id', 'chapter_number', 'chapter_name', 'chapter_image', 'book'
    )
    chapters = list(chapters)
    for chapter in chapters:
        chapter['chapter_image'] = chapter['chapter_image'].url if chapter['chapter_image'] else None

    response_data = {
        'book': {
            'id': book.id,
            'book_number': book.book_number,
            'book_name': book.book_name,
            'book_image': book.book_image.url if book.book_image else None,
        },
        'chapters': chapters
    }
    return JsonResponse(response_data)

def book_chapters(request, book_pk):
    print(f"Received book_pk: {book_pk}")
    book = get_object_or_404(Book, pk=book_pk)
    chapters = Chapter.objects.filter(book=book).values(
        'id', 'chapter_number', 'chapter_name', 'chapter_image'
    )
    chapters = list(chapters)
    for chapter in chapters:
        if chapter['chapter_image']:
            chapter['chapter_image'] = request.build_absolute_uri(settings.MEDIA_URL + str(chapter['chapter_image']))

    response_data = {
        'chapters': chapters
    }
    return JsonResponse(response_data, encoder=DjangoJSONEncoder)

def chapter_detail(request, book_pk, pk):
    chapter = get_object_or_404(Chapter, pk=pk, book_id=book_pk)
    sections = Section.objects.filter(chapter=chapter).values(
        'id', 'section_number', 'section_name', 'section_image', 'chapter'
    )
    sections = list(sections)
    for section in sections:
        section['section_image'] = section['section_image'].url if section['section_image'] else None

    shlokas = Shloka.objects.filter(chapter=chapter).values(
        'id', 'shloka_number', 'shlok_text', 'chapter', 'section'
    )

    response_data = {
        'chapter': {
            'id': chapter.id,
            'chapter_number': chapter.chapter_number,
            'chapter_name': chapter.chapter_name,
            'chapter_image': chapter.chapter_image.url if chapter.chapter_image else None,
            'book': chapter.book_id
        },
        'sections': sections,
        'shlokas': list(shlokas)
    }
    return JsonResponse(response_data)

def section_detail(request, chapter_pk, pk):
    section = get_object_or_404(Section, pk=pk, chapter_id=chapter_pk)
    shlokas = Shloka.objects.filter(section=section).values(
        'id', 'shloka_number', 'shlok_text', 'chapter', 'section'
    )
    
    response_data = {
        'section': {
            'id': section.id,
            'section_number': section.section_number,
            'section_name': section.section_name,
            'section_image': section.section_image.url if section.section_image else None,
            'chapter': section.chapter_id
        },
        'shlokas': list(shlokas)
    }
    return JsonResponse(response_data)

def shloka_detail(request, pk):
    shloka = get_object_or_404(Shloka, pk=pk)
    audio_files = AudioFile.objects.filter(shloka=shloka).values(
        'id', 'file_name', 'file_url'
    )
    
    response_data = {
        'shloka': {
            'id': shloka.id,
            'shloka_number': shloka.shloka_number,
            'shlok_text': shloka.shlok_text,
            'chapter': shloka.chapter_id,
            'section': shloka.section_id
        },
        'audio_files': list(audio_files)
    }
    return JsonResponse(response_data)

def audio_player(request):
    audio_files = AudioFile.objects.all().values(
        'id', 'file_name', 'file_url', 'shloka'
    )
    return JsonResponse(list(audio_files), safe=False)

# Custom exception handler for improved error reporting
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    return response

# ViewSets for REST API

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilterSet

class ChapterViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_pk')
        if book_id:
            return Chapter.objects.filter(book_id=book_id)
        return Chapter.objects.all()

    def retrieve(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_pk')
        if book_id:
            queryset = self.get_queryset()
            chapter = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
            serializer = self.get_serializer(chapter)
            return Response(serializer.data)
        raise NotFound(detail="Book ID not found in request.")

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SectionFilterSet

class ShlokaViewSet(viewsets.ModelViewSet):
    queryset = Shloka.objects.all()
    serializer_class = ShlokaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['chapter', 'section', 'shloka_number']
    search_fields = ['shlok_text']
    ordering_fields = ['shloka_number', 'chapter', 'section']

class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['shloka']
    search_fields = ['file_name']
    ordering_fields = ['shloka', 'file_name']
