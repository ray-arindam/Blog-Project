from django.urls import path,include
from blog import views

app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('blog/',views.blog,name='blog'),
    path('post/<int:id>/',views.post,name='post-detail'),
    path('create/',views.post_create,name='post-create'),
    path('post/<int:id>/update/',views.post_update,name='post-update'),
    path('post/<int:id>/delete/',views.post_delete,name='post-delete'),
    path('search/',views.search,name='search'),

]