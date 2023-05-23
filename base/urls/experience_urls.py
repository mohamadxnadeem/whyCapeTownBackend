from django.urls import path
from base.views import experience_views as views


urlpatterns = [
    path('', views.getExperiences, name='experiences'),
    path('create/', views.createExperience, name='experience-create'),
    path('upload/', views.uploadImage, name='image-upload'),
    path('top/', views.getTopExperiences, name='top-experiences'),
    path('<str:pk>/reviews/', views.createExperienceReview, name='create-experience-review'),
    path('<str:pk>/', views.getExperience, name='experience'),
    path('update/<str:pk>/', views.updateExperience, name='experience-update'),
    path('delete/<str:pk>/', views.deleteExperience, name='experience-delete'),

]