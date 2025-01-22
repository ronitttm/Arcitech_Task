from django.urls import path
from .views import RegisterAuthorView, LoginView, ContentListCreateView, ContentDetailView, ContentSearchView, AdminContentListView, AdminContentDetailView

urlpatterns = [
    path('register/', RegisterAuthorView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('content/', ContentListCreateView.as_view(), name='content-create'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='content-detail'),
    path('content/search/', ContentSearchView.as_view(), name='content-search'),
    path('admin/content/', AdminContentListView.as_view(), name='admin-content-list'),
    path('admin/content/<int:pk>/', AdminContentDetailView.as_view(), name='admin-content-detail'),
]
