from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

#defining the urls for the catai app
urlpatterns = [
    #the home page of the catai app
    #'' means the root path
    path('', views.home, name='home'), 
    #the about page of the catai app
    path('about/', views.about, name='about'),
    path('facts/', views.facts, name='facts'),
    path('history/', views.history, name='history'),
    #delte the image from the database and the media folder
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
