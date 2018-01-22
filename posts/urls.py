from django.conf.urls import url
from django.contrib import admin

from .views import(post_list,
	post_create,
	post_delete,
	post_update,
	post_details

	)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list,name="list"),
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_details,name="details"),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update,name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete,name="delete"),

]
