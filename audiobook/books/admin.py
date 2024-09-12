from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Book, Chapter, Section, Shloka, AudioFile, Role

class ShlokaInline(admin.TabularInline):
    model = Shloka
    extra = 3  # Adjust the number of extra forms as needed

class SectionInline(admin.TabularInline):
    model = Section
    extra = 3  # Adjust the number of extra forms as needed
    inlines = [ShlokaInline]

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 3  # Adjust the number of extra forms as needed
    inlines = [SectionInline]

class BookAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]
    list_display = ('id','book_number', 'book_name', 'book_image', 'created_at', 'modified_at', 'modified_by')
    search_fields = ('book_name',)
    list_filter = ('created_at', 'modified_at', 'modified_by')

    def save_model(self, request, obj, form, change):
        if Book.objects.filter(book_number=obj.book_number).exclude(id=obj.id).exists():
            raise ValidationError(f"Book number {obj.book_number} already exists.")
        super().save_model(request, obj, form, change)

class ChapterAdmin(admin.ModelAdmin):
    inlines = [SectionInline]
    list_display = ('id','book', 'chapter_number', 'chapter_name', 'chapter_image', 'created_at', 'modified_at', 'modified_by')
    search_fields = ('chapter_name', 'book__book_name')
    list_filter = ('book', 'created_at', 'modified_at')

    def save_model(self, request, obj, form, change):
        if Chapter.objects.filter(book=obj.book, chapter_number=obj.chapter_number).exclude(id=obj.id).exists():
            raise ValidationError(f"Chapter number {obj.chapter_number} already exists in this book.")
        super().save_model(request, obj, form, change)

class SectionAdmin(admin.ModelAdmin):
    inlines = [ShlokaInline]
    list_display = ('chapter', 'section_number', 'section_name', 'section_image', 'created_at', 'modified_at', 'modified_by')
    search_fields = ('section_name', 'chapter__chapter_name')
    list_filter = ('chapter', 'created_at', 'modified_at')

    def save_model(self, request, obj, form, change):
        if Section.objects.filter(chapter=obj.chapter, section_number=obj.section_number).exclude(id=obj.id).exists():
            raise ValidationError(f"Section number {obj.section_number} already exists in this chapter.")
        super().save_model(request, obj, form, change)

class ShlokaAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'section', 'shloka_number','shlok_text', 'audio', 'created_at', 'modified_at', 'modified_by')
    search_fields = ('shlok_text', 'chapter__chapter_name', 'section__section_name')
    list_filter = ('chapter', 'section', 'created_at', 'modified_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'text_file')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'created_at', 'modified_at', 'modified_by')
    search_fields = ('role_name',)
    list_filter = ('created_at', 'modified_at')

admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Shloka, ShlokaAdmin)
admin.site.register(AudioFile, AudioFileAdmin)
admin.site.register(Role, RoleAdmin)
