from django.conf.urls import url
from .views import CustomerViewSet, CustomersViewSet
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^(?P<pk>[\w\.-]+)/$', CustomerViewSet.as_view()),
    url(r'^$', CustomersViewSet.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
