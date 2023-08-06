from django.conf.urls import url

from .views.api.aiu import AIU

from . import views
from .views import aiu

urlpatterns = [
    url(r'^$', aiu.index, name='aiu'),
    url(r'^api/v1/aiu/(?P<term_id>\d{4}-(winter|spring|summer|autumn))'
        r'(\.(?P<format>txt|json))?$', AIU().run),
]
