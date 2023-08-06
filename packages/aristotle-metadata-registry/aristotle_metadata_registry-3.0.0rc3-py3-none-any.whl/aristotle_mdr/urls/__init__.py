from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^', include('aristotle_mdr.contrib.issues.urls', namespace="aristotle_issues")),
    url(r'^', include('aristotle_mdr.contrib.publishing.urls', app_name="aristotle_mdr_publishing", namespace="aristotle_publishing")),
    url(r'^', include('aristotle_mdr.urls.base')),
    url(r'^browse/', include('aristotle_mdr.contrib.browse.urls')),
    url(r'^favourites/', include('aristotle_mdr.contrib.favourites.urls', namespace="aristotle_favourites")),
    url(r'^help/', include('aristotle_mdr.contrib.help.urls', app_name="aristotle_help", namespace="aristotle_help")),
    url(r'^', include('aristotle_mdr.contrib.user_management.urls', namespace="aristotle-user")),
    url(r'^', include('aristotle_mdr.urls.aristotle', app_name="aristotle_mdr", namespace="aristotle")),
    url(r'^ac/', include('aristotle_mdr.contrib.autocomplete.urls', namespace="aristotle-autocomplete")),
    url(r'^', include('aristotle_mdr.contrib.healthcheck.urls', app_name="aristotle_mdr_hb", namespace="aristotle_hb")),
    url(r'^', include('aristotle_mdr.contrib.view_history.urls')),
    url(r'^api/', include('aristotle_mdr_api.urls'))
]

# This is only for dev work, so we can skip it.
if settings.DEBUG:  # pragma: no cover
    from django.contrib.staticfiles import views

    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]

    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'aristotle_mdr.views.unauthorised'
handler404 = 'aristotle_mdr.views.not_found'
handler500 = 'aristotle_mdr.views.handler500'
