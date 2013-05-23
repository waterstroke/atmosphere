import os

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url, include


from rest_framework.urlpatterns import format_suffix_patterns

from api.identity import IdentityList, Identity, IdentityDetailList
from api.instance import InstanceList, Instance, InstanceAction
from api.notification import NotificationList
from api.machine import MachineList, Machine
from api.machine_request import MachineRequestList, MachineRequest,\
    MachineRequestAction
from api.machine_export import MachineExportList, MachineExport
from api.size import SizeList, Size
from api.volume import VolumeList, Volume
from api.profile import Profile
from api.occupancy import Occupancy
from api.provider import ProviderList, Provider
from api.user import UserManagement, User
from api.group import GroupList, Group
from api.tag import TagList, Tag
from api.meta import Meta, MetaAction
from api.version import Version
from api.root import APIRoot

from authentication.decorators import atmo_valid_token_required

resources_path = os.path.join(os.path.dirname(__file__), 'resources')
mobile = os.path.join(os.path.dirname(__file__), 'mobile')
cloud2 = os.path.join(os.path.dirname(__file__), 'cf2')

admin.autodiscover()
urlpatterns = patterns(
    '',
    #Uncomment the next line to enable the admin control panel
    #admin logging, and admin user emulation
    url(r'^admin/emulate/$', 'web.views.emulate_request'),
    url(r'^admin/emulate/(?P<username>\w+)/$', 'web.views.emulate_request'),
    #url(r'^admin/logs/', 'web.views.logs'),
    url(r'^admin/', include(admin.site.urls)),

    # feedback
    url(r'^feedback', 'web.emails.feedback'),
    url(r'^api/email_support', 'web.emails.email_support'),

    #v2 api url scheme
    url(r'^auth/$', 'authentication.views.authenticate'),

    #This is a TEMPORARY url..
    #In v2 this is /api/provider/<id>/identity/<id>/instance/action
    #&& POST['action'] = request_image
    url(r'^api/request_quota/$', 'web.emails.requestQuota'),
    url(r'^api/request_image/$', 'web.emails.requestImaging'),

    # static files
    url(r'^init_files/(?P<file_location>.*)$', 'web.views.get_resource'),

    # Systemwide
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': resources_path}),

    # instance service
    url(r'^instancequery/', 'web.views.ip_request'),

    # default
    url(r'^$', 'web.views.redirectApp'),

    #This URL validates the ticket returned after CAS login
    url(r'^CAS_serviceValidater', 'authentication.protocol.cas.cas_validateTicket'),
    #This URL is a dummy callback
    url(r'^CAS_proxyCallback', 'authentication.protocol.cas.cas_proxyCallback'),
    #This URL records Proxy IOU & ID
    url(r'^CAS_proxyUrl', 'authentication.protocol.cas.cas_storeProxyIOU_ID'),

    url(r'^login/$', 'web.views.login'),
    url(r'^logout/$', 'web.views.logout'),
    url(r'^CASlogin/(?P<redirect>.*)$', 'authentication.cas_loginRedirect'),
    url(r'^application/$', 'web.views.app'),

    url(r'^partials/(?P<path>.*)$', 'web.views.partial'),
    url(r'^no_user/$', 'web.views.no_user_redirect'),

    ### DJANGORESTFRAMEWORK ###
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += format_suffix_patterns(patterns(
    '',
    url(r'api/$', APIRoot.as_view()),
    url(r'api/version/$', Version.as_view()),
    url(r'^api/notification/$', NotificationList.as_view()),

    url(r'^api/user/$', atmo_valid_token_required(UserManagement.as_view())),
    url(r'^api/user/(?P<username>.*)/$', User.as_view()),
    url(r'^api/profile/$', Profile.as_view(), name='profile'),
    url(r'^api/provider/(?P<provider_id>.*)/occupancy/$', Occupancy.as_view()),

    url(r'^api/group/$', GroupList.as_view()),
    url(r'^api/group/(?P<groupname>.*)/$', Group.as_view()),

    url(r'^api/tag/$', TagList.as_view()),
    url(r'^api/tag/(?P<tag_slug>.*)/$', Tag.as_view()),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/image_export/$',
        MachineExportList.as_view(), name='machine-export-list'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/image_export/(?P<machine_request_id>.*)/$',
        MachineExport.as_view(), name='machine-export'),

    url(r'^api/provider/(?P<provider_id>.*)/identity/'
        + '(?P<identity_id>.*)/request_image/$',
        MachineRequestList.as_view(), name='machine-request-list'),
    url(r'^api/provider/(?P<provider_id>.*)/identity/'
        + '(?P<identity_id>.*)/request_image/(?P<machine_request_id>.*)/$',
        MachineRequest.as_view(), name='machine-request'),

    url(r'^api/request_image/(?P<machine_request_id>.*)/(?P<action>.*)/$',
        MachineRequestAction.as_view(), name='machine-request-detail'),

    url(r'^api/provider/(?P<provider_id>.*)/identity/'
        + '(?P<identity_id>.*)/profile/$',
        Profile.as_view(), name='profile-detail'),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/instance/(?P<instance_id>.*)/action/$',
        InstanceAction.as_view(), name='instance-action'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/instance/(?P<instance_id>.*)/$',
        Instance.as_view(), name='instance-detail'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/instance/$',
        InstanceList.as_view(), name='instance-list'),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/size/$',
        SizeList.as_view(), name='size-list'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/size/(?P<size_id>.*)/$',
        Size.as_view(), name='size-detail'),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/volume/$',
        VolumeList.as_view(), name='volume-list'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/volume/(?P<volume_id>.*)/$',
        Volume.as_view(), name='volume-detail'),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/machine/$',
        MachineList.as_view(), name='machine-list'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/machine/(?P<machine_id>.*)/$',
        Machine.as_view(), name='machine-detail'),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/meta/$', Meta.as_view(), name='meta-detail'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/meta/(?P<action>.*)/$',
        MetaAction.as_view(), name='meta-action'),

    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/$', IdentityList.as_view(), name='identity-list'),
    url(r'^api/provider/(?P<provider_id>.*)/identity'
        + '/(?P<identity_id>.*)/$',
        Identity.as_view(), name='identity-detail'),

    url(r'^api/identity/$', IdentityDetailList.as_view(), name='identity-detail-list'),

    url(r'^api/provider/$', ProviderList.as_view(), name='provider-list'),
    url(r'^api/provider/(?P<provider_id>.*)/$',
        Provider.as_view(), name='provider-detail'),

))

urlpatterns += staticfiles_urlpatterns()
