from django.urls import path
from base.views import accounts_views as views

urlpatterns = [
  path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('register/',views.registerUser, name='register'),
  path('profile/', views.getUserProfile, name="users-profile"),
  path('profile/update/', views.updateUserProfile, name="user-profile-update"),
  path('<str:pk>/', views.getUserById, name='user'),
  path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
  path('search_id/', views.find_user_id, name='user-find'),
  # path('search_id/', views.MyTokenObtainWithEmailView.as_view(), name='token_obtain_email'),
] 
