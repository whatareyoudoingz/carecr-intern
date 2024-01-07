from django.urls import path
from base.views import posts_views as views

urlpatterns = [
  path('', views.getPosts, name='posts'),
  path('create/', views.createPosts, name='posts-create'),
  path('<str:pk>/reviews/',views.getPostsReview, name='review'),
  path('<str:pk>/reviews/create/',views.createPostsReview, name='create-review'),
  path('<str:pk>/', views.getPost, name='post'),
  path('update/<str:pk>/', views.updatePosts, name='posts-update'),
  path('delete/<str:pk>/',views.deletePosts, name='posts-delete')
]