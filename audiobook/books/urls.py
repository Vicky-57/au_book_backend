from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # Correct router import
from .views import (
    book_list, book_detail, chapter_detail, section_detail, 
    shloka_detail, audio_player, book_chapters, BookViewSet, ChapterViewSet, 
    SectionViewSet, ShlokaViewSet, AudioFileViewSet
)

# Main router for books
router = DefaultRouter()
router.register(r'books', BookViewSet)

# Nested router for chapters under books
book_router = NestedDefaultRouter(router, r'books', lookup='book')
book_router.register(r'chapters', ChapterViewSet, basename='book-chapters')

# Register additional viewsets with the main router
router.register(r'sections', SectionViewSet)
router.register(r'shlokas', ShlokaViewSet)
router.register(r'audiofiles', AudioFileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_list, name='book_list'),
    
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('book/<int:book_pk>/chapters/', book_chapters, name='book_chapters'),  # No need for 'views.'
    
    path('book/<int:book_pk>/chapter/<int:pk>/', chapter_detail, name='chapter_detail'),
    path('chapter/<int:chapter_pk>/section/<int:pk>/', section_detail, name='section_detail'),
    path('shloka/<int:pk>/', shloka_detail, name='shloka_detail'),
    
    # API routes
    path('api/', include(router.urls)),
    path('api/', include(book_router.urls)),  # Include nested routes
]
