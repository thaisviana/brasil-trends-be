from django.core.management.base import BaseCommand, CommandError
from elections.models import Word, Category
from django.db.models import Q
import requests
import os
import json
import time

class Command(BaseCommand):
    help = 'Categorize words using Gemini API'

    def handle(self, *args, **options):
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            self.stdout.write(self.style.ERROR('GOOGLE_API_KEY environment variable not set.'))
            return

        categories = list(Category.objects.values_list('text', flat=True))
        categories_str = ', '.join(categories)
        
        # Filter words that need categorization
        # words = Word.objects.filter(Q(category__isnull=True) | Q(category__text='Outros'), status=True)
        # Based on original code:
        words = Word.objects.filter(Q(category__isnull=True) | Q(category_id=2), candidate__second_round=True)
        
        total = words.count()
        self.stdout.write(f'Found {total} words to categorize.')
        
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}'
        headers = {'Content-Type': 'application/json'}

        for i, word in enumerate(words):
            candidate_name = word.candidate.name if word.candidate else "Unknown"
            
            prompt = (
                f"Categorize the word/phrase '{word.text}' related to the political candidate '{candidate_name}'. "
                f"Choose one of the following categories: {categories_str}. "
                f"If none fit well, suggest a new short category name (max 3 words). "
                f"Return ONLY the category name, nothing else."
            )
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    result = response.json()
                    try:
                        category_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                        # Remove any punctuation or extra spaces
                        category_text = category_text.replace('.', '').replace('"', '').strip()
                        
                        category, created = Category.objects.get_or_create(text=category_text)
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Created new category: {category_text}'))
                        
                        word.category = category
                        word.save()
                        self.stdout.write(f'[{i+1}/{total}] Categorized "{word.text}" as "{category_text}"')
                        
                    except (KeyError, IndexError) as e:
                        self.stdout.write(self.style.ERROR(f'Error parsing response for "{word.text}": {e}'))
                elif response.status_code == 429:
                    self.stdout.write(self.style.WARNING('Rate limit exceeded. Waiting 60 seconds...'))
                    time.sleep(60)
                else:
                    self.stdout.write(self.style.ERROR(f'API Error {response.status_code}: {response.text}'))
                
                # Simple rate limiting to avoid hitting default quotas too hard
                time.sleep(1)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Request failed: {str(e)}'))
