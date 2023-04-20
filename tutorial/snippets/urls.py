from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('snippets/', views.snippet_list),  # function views
    # path('snippets/<int:pk>/', views.snippet_detail),  # function views
    path('snippets/', views.SnippetList.as_view()),  # class views
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),  # class views
]

urlpatterns = format_suffix_patterns(urlpatterns)
