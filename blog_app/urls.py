from django.urls import path
from . import views

urlpatterns = [
    path('',views.aboutview.as_view(),name='about'),
    path('post/',views.postlistview.as_view(),name='post_list'),
    #path('post/Upost/',views.upostlistview.as_view(),name='Ulist'),#post list for the individual user
    path('post/<int:pk>',views.postdetailview.as_view(),name='post_detail'),#<int:pk> is specified so that the primary key for that post is specified and only that post is accessed
    path('post/create',views.postcreateview.as_view(),name='post_create'),
    path('post/<int:pk>/edit/',views.postupdateview.as_view(),name='post_update'),
    #here the pk is specifed in the middle so that only that post is updated
    path('post/<int:pk>/remove/',views.postdeleteview.as_view(),name='post_remove'),
    path('post/<int:pk>/publish/',views.post_publish,name='post_publish'),
    path('post/<int:pk>/comment/',views.add_comment,name='add_comment'),
    #use the comment path to specify which comment has to be rejected
    path('comment/<int:pk>/reject/',views.com_reject,name='com_reject'),

   path('post/Upost/',views.upostview,name='Ulist'),#post list for the individual user

    # path('post/create',views.createview,name='post_create'),

## the level or order of the pk depends on the foreignkey for the models
    # ex:comment model has foreignkey 'post' so the query(comment) number will be for the individual post
    # post model has foreginkey 'userinfo'(users) so the posts correspond to the particular user
# keep a note on the url names as they will be used in the template url tagging


]