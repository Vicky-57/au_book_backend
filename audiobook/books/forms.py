from django import forms
from .models import Book, Chapter, Section, Shloka, AudioFile

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_number', 'book_name', 'book_image']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['book', 'chapter_number', 'chapter_name', 'chapter_image']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['chapter', 'section_number', 'section_name', 'section_image']

class ShlokaForm(forms.ModelForm):
    class Meta:
        model = Shloka
        fields = ['chapter', 'section', 'shlok_text', 'audio_file', 'text_file']

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['file_path', 'file_format']
