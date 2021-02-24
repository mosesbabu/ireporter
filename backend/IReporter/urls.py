from django.conf.urls import url
from . import views
from django.urls import path,re_path 
from .views import FlagDetail,FlagStatus,AllFlagRecords,CreateFlag,FlagList
from .views import CreateUserAPIView,LoginApiView,ProfileList,SingleProfile,TagList,TagDetail
from django.urls import path,re_path 
from .views import InterventionList, CreateInterventionRecord, InterventionDetail, InterventionListStatus,AllInterventionRecords
app_name='IReporter'
urlpatterns=[
    url(r'^api/signup/$', CreateUserAPIView.as_view()),
    url(r'^api/login/$', LoginApiView.as_view()),
    url(r'^api/profiles/$',ProfileList.as_view(),name="profilelist"),
    url(r'^api/profile/(?P<pk>[0-9]+)$',SingleProfile.as_view(),name="singleprofile"),
    url(r'^api/intervention-record/create/$', CreateInterventionRecord.as_view(), name='create-intervention-item'),
    url(r'^api/intervention-records/$',AllInterventionRecords.as_view(), name='AllInterventionRecords'),
    url(r'^api/intervention-record/search/[\s]*(.*?)[\s]*/$',InterventionList.as_view(), name='fetch-intervention-records'),
    url(r'^api/intervention-record/detail/(?P<pk>[0-9]+)$',InterventionDetail.as_view(), name='intervention-detail'),
    url(r'^api/intervention-records/status/(?P<intervention_status>[A-Za-z]+)$' ,InterventionListStatus.as_view(), name='filter-by-status'),
    url(r'^api/flags/create/$',CreateFlag.as_view()),
    url(r'^api/flags/$',AllFlagRecords.as_view(),name='allflags'),
    url(r'^api/flag/detail/(?P<pk>[0-9]+)$',FlagDetail.as_view()),
    url(r'^api/flag/search/[\s]*(.*?)[\s]*/$',FlagList.as_view(), name='fetch flag records'),
    url(r'^api/tags/$', TagList.as_view()),
    url(r'^api/tag/(?P<pk>[0-9]+)$', TagDetail.as_view()),
]

        
