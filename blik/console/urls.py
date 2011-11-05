from django.conf.urls.defaults import *
from console_base.views import *
from utils import get_media
import django.conf.urls.i18n
from console_base.auth import authenticate_user

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     (r'^$', index),
     (r'^static/(.+)$', get_media),
     (r'^get_menu_items/$', get_menu_items),
     (r'^auth/$', authenticate_user),
     (r'^clusters_list/$', get_clusters_list),
     (r'^cluster_config/(\d+)$', configure_cluster),
     (r'^change_cluster_parameters/(\d+)$', change_cluster_params),
)
