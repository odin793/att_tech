from django.conf.urls import patterns, include, url
from att_tech_app.views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'att_tech.views.home', name='home'),
    # url(r'^att_tech/', include('att_tech.foo.urls')),
    url(r'^$', index_page, name="index_url"),
    url(r'^about_tech/(about_tech)/$', basic_page_view, name="about_tech"),
    url(r'^about_tech/(structure)/$', page_with_docs_view, name="structure"),
    url(r'^about_tech/(constituent_docs)/$', page_with_docs_view,
        name="constituent_docs"),
    url(r'^about_tech/employees/$', employees_page, name="employees_page"),
    url(r'^about_tech/masters/$', masters_page, name="masters_page"),
    url(r'^matriculants/profs_and_specs/$', profs_and_specs_page,
        name="profs_and_specs"),
    url(r'^matriculants/(docs_samples)/$', page_with_docs_view,
        name="docs_samples"),
    url(r'^matriculants/(acceptance)/$', page_with_docs_view,
        name="acceptance"),
    url(r'^matriculants/(tuition_by_correspondence)/$', basic_page_view,
        name="tuition_by_correspondence"),
    url(r'^matriculants/(courses)/$', basic_page_view, name="courses"),
    url(r'^matriculants/(acceptance_rules)/$', basic_page_view,
        name="acceptance_rules"),
    url(r'^students/(schedule)/$', page_with_docs_view, name="schedule"),
    url(r'^students/(stud_life)/$', news_page, name="stud_life_page"),
    url(r'^students/(stud_life)/(\w+)/$', exact_new, name="exact_stud_life"),
    url(r'^contacts/$', contacts_page, name="contacts"),
    url(r'^news/(news)/$', news_page, name="news_page"),
    url(r'^news/(news)/(\w+)/$', exact_new, name="exact_new"),
    #url(r'^about_tech/$', about_tech, name="about_tech_url"),
    (r'^tinymce/', include('tinymce.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )