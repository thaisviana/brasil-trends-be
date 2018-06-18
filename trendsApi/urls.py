
from hybridrouter import HybridRouter
from elections.api import router
from django.conf.urls import url, include


root_router = HybridRouter()

root_router.register_router(router)
urlpatterns = [
    url(r'^v1/', include((root_router.urls, 'elections'), namespace='v1')),

]
