"""squery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from samplequery import views
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title = 'Pastebin API')


# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter(trailing_slash=True)
router.register(r'users', views.UserViewSet)
router.register(r'record',views.RecordViewSet)
router.register(r'tissue',views.TissuesViewSet)
router.register(r'panel',views.PanelViewSet)

# urlpatterns = [
#     url(r'^$',views.api_root,name='api-root'),
#     url(r'^api/',include(router.urls)),
#     url(r'^admin/', admin.site.urls),
#     #url(r'^$',views.index),
#     url(r'^record/$',views.RecordList.as_view(),name='record-list'),
#     url(r'^record/id/(?P<pk>[0-9]+)/$',views.RecordDetail.as_view(),name='record-detail'),
#     url(r'^record/fid/(?P<full_id>[\d\w]+)/$',views.RecordDetail.as_view(),name='record-detail'),
#     url(r'^tissue/$',views.TissuesList.as_view(),name='tissues-list'),
#     url(r'^tissue/(?P<pk>cfDNA|FFPE|Normal)/$',views.TissuesDetail.as_view(),name='tissues-detail'),
#     url(r'^panel/$',views.PanelList.as_view(),name='panel-list'),
#     url(r'^panel/(?P<pk>[\d\w]+)/$',views.PanelDetail.as_view(),name='panel-detail'),
#     url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
# ]

urlpatterns = [
    url(r'^',include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    url(r'^schema/$',schema_view),
    url(r'^query',views.query,name='query'),
    # url(r'^q/',views.RecordListView.as_view())
    # url(r'^samplequery/query/',views.post_query,name='post-query')
]