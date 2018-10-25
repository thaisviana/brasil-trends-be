from rest_framework import routers
from .candidate_words import CandidateViewSet, WordViewSet
from .category import CategoryViewSet
from .candidate import CandidateLightViewSet
from .important_dates import ImportantDatesViewSet
from .relationship import list_relationship_view
from .line_candidate import list_individual_lines_view
from .line_all import list_aggregated_lines_view
from .category_radar import radar_view, radar_r2_view
from .new_category_radar import new_radar_view
from .category_bar import bar_view, bar_r2_view
from .orbit import orbit_view
from .words_category import WordCategoryViewSet

router = routers.SimpleRouter()

router.register(r'infos', CandidateLightViewSet, 'infos')
router.register(r'dates', ImportantDatesViewSet, 'dates')
router.register(r'candidate', CandidateViewSet, 'candidate')
router.register(r'word', WordViewSet, 'word')
router.register(r'word_category', WordCategoryViewSet, 'word_category')
router.register(r'category', CategoryViewSet, 'category')
