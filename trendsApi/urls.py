
from hybridrouter import HybridRouter
from elections.api import router
from django.conf.urls import url, include
from elections.api import list_relationship_view, radar_view, orbit_view,bar_r2_view, \
    bar_view, list_individual_lines_view, list_aggregated_lines_view, new_radar_view, radar_r2_view


root_router = HybridRouter()

root_router.register_router(router)
urlpatterns = [
    url(r'^v1/', include((root_router.urls, 'elections'), namespace='v1')),
    url(r'^v1/relationship/$', list_relationship_view, name='list_relationship'),
    url(r'^v1/candidate_line/$', list_individual_lines_view, name='candidate_line'),
    url(r'^v1/aggregated_line/$', list_aggregated_lines_view, name='aggregated_line'),
    url(r'^v1/radar/$', radar_view, name='radar'),
    url(r'^r2/radar/$', radar_r2_view, name='r2_radar'),
    url(r'^v1/new_radar/$', new_radar_view, name='new_radar'),
    url(r'^v1/new_bar/$', bar_view, name='new_bar'),
    url(r'^r2/bar/$', bar_r2_view, name='r2_bar'),
    url(r'^v1/orbit/$', orbit_view, name='orbit'),

]
