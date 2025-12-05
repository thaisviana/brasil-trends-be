from django.contrib import admin
from .models import Candidate, Word, Category, ImportantDates, SizeHistory, SizeHistorySecondRound

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active', 'election_year')
    search_fields = ('name', 'slug')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'candidate', 'size', 'period')
    search_fields = ('text', 'candidate__name')
    list_filter = ('period', 'candidate')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(ImportantDates)
class ImportantDatesAdmin(admin.ModelAdmin):
    list_display = ('text', 'date', 'confirmed')

@admin.register(SizeHistory)
class SizeHistoryAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'date', 'weekly_size')
    list_filter = ('candidate',)

@admin.register(SizeHistorySecondRound)
class SizeHistorySecondRoundAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'date', 'size')
    list_filter = ('candidate',)
