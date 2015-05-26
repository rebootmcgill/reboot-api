from django.conf.urls import patterns, url, include
from rebootAPI import views

router = views.get_router()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^stats/$', views.StatsAPI.as_view()),
)
