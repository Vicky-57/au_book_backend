from rest_framework import serializers
from .models import Book, Chapter, Section, Shloka, AudioFile

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'

class ShlokaSerializer(serializers.ModelSerializer):
    audio = AudioFileSerializer()  # Ensure this matches the model field name

    class Meta:
        model = Shloka
        fields = ['id', 'shloka_number', 'shlok_text', 'audio', 'chapter', 'section']

class SectionSerializer(serializers.ModelSerializer):
    shlokas = ShlokaSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'section_number', 'section_name', 'section_image', 'shlokas', 'chapter']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        # Add 'sections' to the fields list
        fields = ['id', 'chapter_number', 'chapter_name', 'chapter_image', 'book']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'book_number', 'book_name', 'book_image']
