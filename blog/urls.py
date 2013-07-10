from django.conf.urls import patterns, include, url
from django.views.generic import list_detail
from blog_app.models import Blog

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from blog_app.views import home,register,archive_view,usrlogout,postbyuser,post_view,new_post,post_edit

post_list_info={
    'queryset':Blog.objects.order_by("-created"),
    'template_name':'viewpost.html',
}

urlpatterns = patterns('',(r'^$',home),(r'^register/$',register),(r'^viewposts/$',list_detail.object_list,post_list_info),
    (r'^archive/$',archive_view),(r'^logout/$',usrlogout),(r'^post/(\d+)/$',post_view),
    (r'^newpost/$',new_post),(r'^postedit/(\d+)/$',post_edit),(r'^([A-Za-z\d]+)/posts/$',postbyuser),
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
