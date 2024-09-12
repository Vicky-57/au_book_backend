from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book, Chapter, Section, Shloka, AudioFile

class BookChapterSectionAPITestCase(APITestCase):

    def setUp(self):
        self.book = Book.objects.create(book_number=1, book_name='Test Book')
        self.chapter = Chapter.objects.create(book=self.book, chapter_number=1, chapter_name='Test Chapter')
        self.section = Section.objects.create(chapter=self.chapter, section_number=1, section_name='Test Section')
        self.shloka = Shloka.objects.create(
            chapter=self.chapter, 
            section=self.section, 
            shloka_number=1, 
            shlok_text='Test Shloka'
        )
        self.book_url = reverse('book-list')
        self.chapter_url = reverse('chapter-list')
        self.section_url = reverse('section-list')
        self.shloka_url = reverse('shloka-list')

    def test_get_book_list(self):
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['book_name'], 'Test Book')

    def test_get_chapter_list(self):
        response = self.client.get(self.chapter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['chapter_name'], 'Test Chapter')

from django.http import JsonResponse
from .models import Book

def get_books(request):
    books = Book.objects.all()  # Fetch all books
    data = list(books.values('book_number', 'book_name'))  # Convert to a list of dictionaries
    return JsonResponse(data, safe=False)
