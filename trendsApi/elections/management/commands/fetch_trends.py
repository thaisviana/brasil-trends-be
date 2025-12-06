from django.core.management.base import BaseCommand
from pytrends.request import TrendReq
import pandas as pd
import traceback
from elections.service import ElectionService
from elections.models import Candidate

class Command(BaseCommand):
    help = 'Fetch related queries from Google Trends for a given term'

    def add_arguments(self, parser):
        parser.add_argument('term', type=str, help='The search term or "all" for all active candidates')
        parser.add_argument('timeframe', type=str, help='today 12-m')
        
    def fetch_data_for_term(self, term, timeframe, proxy):
        self.stdout.write(f'Fetching trends for: {term}...')
        if proxy:
            self.stdout.write(f'Using proxy: {proxy}')

        try:
            # Initialize TrendReq with custom session and proxy
            pytrends = TrendReq(hl='pt-BR', tz=360, proxies=[proxy] if proxy else [])
            
            pytrends.build_payload([term], cat=0, timeframe=timeframe, geo='BR', gprop='')
            
            # Map timeframe to database period code
            timeframe_map = {
                'now 1-d': 'TDY',
                'now 7-d': 'WKK',
                'today 1-m': 'MNT',
                'today 12-m': 'YAR'
            }
            db_period = timeframe_map.get(timeframe, 'YAR') # Default to YAR if not found
            
            related_queries = pytrends.related_queries()
            
            if related_queries and term in related_queries:
                self.stdout.write(self.style.SUCCESS(f'Successfully fetched related queries for "{term}"'))
                
                top = related_queries[term]['top']
                rising = related_queries[term]['rising']
                
                # print(related_queries)
                
                candidate = ElectionService.get_candidate_by_name(term)
                if candidate:
                    self.stdout.write(self.style.SUCCESS(f'Found candidate: {candidate.name}'))
                    count = 0
                    
                    if top is not None:
                        self.stdout.write('\n--- TOP QUERIES ---')
                        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                            print(top.head(10))
                        
                        for index, row in top.iterrows():
                            ElectionService.process_and_save_word(candidate, row['query'], row['value'], db_period)
                            count += 1

                    if rising is not None:
                        self.stdout.write('\n--- RISING QUERIES ---')
                        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                            print(rising.head(10))
                            
                        for index, row in rising.iterrows():
                            try:
                                value = int(row['value'])
                            except ValueError:
                                value = 100 # Default for 'Breakout' or similar
                            
                            ElectionService.process_and_save_word(candidate, row['query'], value, db_period)
                            count += 1
                    
                    self.stdout.write(self.style.SUCCESS(f'Saved {count} words for candidate {candidate.name}'))
                    
                    # Fetch Interest Over Time
                    self.stdout.write('Fetching interest over time...')
                    interest_over_time = pytrends.interest_over_time()
                    
                    if not interest_over_time.empty:
                        self.stdout.write(self.style.SUCCESS('Successfully fetched interest over time'))
                        
                        history_count = 0
                        for index, row in interest_over_time.iterrows():
                            if term in row:
                                value = row[term]
                                ElectionService.process_and_save_size_history(candidate, index, value)
                                history_count += 1
                        
                        self.stdout.write(self.style.SUCCESS(f'Saved {history_count} history entries for candidate {candidate.name}'))
                    else:
                        self.stdout.write(self.style.WARNING('Interest over time data is empty'))

                else:
                    self.stdout.write(self.style.WARNING(f'No candidate found for "{term}". Words will NOT be saved to database.'))
                    
                    if top is not None:
                        self.stdout.write('\n--- TOP QUERIES ---')
                        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                            print(top.head(10))
                    
                    if rising is not None:
                        self.stdout.write('\n--- RISING QUERIES ---')
                        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                            print(rising.head(10))

            else:
                self.stdout.write(self.style.WARNING(f'No related queries found for "{term}"'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching trends for {term}: {str(e)}'))
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            
            if '429' in str(e):
                self.stdout.write(self.style.WARNING(
                    '\n[!] Google returned a 429 "Too Many Requests" error.\n'
                    'This means your IP is temporarily blocked from making requests to Google Trends.\n'
                    'Suggestions:\n'
                    '1. Wait a few minutes and try again.\n'
                    '2. Use a proxy with the --proxy argument.\n'
                    '3. Try a different network (e.g., mobile data).'
                ))

    def handle(self, *args, **kwargs):
        term = kwargs['term']
        timeframe = kwargs['timeframe']
        if not timeframe:
            timeframe = 'today 12-m'

        proxy = 'https://td-customer-xvlMUjfc9bjt-country-br-state-goiás-city-caldasnovas-asn-AS14840-sessid-brqcslaubl6gaa635-sesstime-10:wsqTOjb6jbtu@j3yyrisl.na.thordata.net:9999'

        if term.lower() == 'all':
            candidates = Candidate.objects.filter(active=True)
            self.stdout.write(f'Fetching trends for all {candidates.count()} active candidates...')
            for candidate in candidates:
                self.fetch_data_for_term(candidate.name, timeframe, proxy)
        else:
            self.fetch_data_for_term(term, timeframe, proxy)
