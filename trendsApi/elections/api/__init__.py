from rest_framework import routers
from .candidate_words import CandidateViewSet, WordViewSet

router = routers.SimpleRouter()

router.register(r'candidate', CandidateViewSet, 'candidate')
router.register(r'word', WordViewSet, 'word')
