from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',Landing_1, name='Landing_1'),
    path('',HomeView, name='home'),
    path('getstream/', Stream, name='streamdt'),
    path('gettokenstream/<token>', StreamToken, name='streamtk'),
    path('stream/', StreamView, name='streamroom'),
    path('streamtoken/<token>', StreamTokenView, name='stokenview'),
    path('api/', APIEnd, name='api'),
    path('Deploy_8/',Deploy_8, name='Deploy_8'),
    path('Database/',Database,name='Database'),
    path('Register_2/', Register_2, name='Register_2'),
    path('Login_3/', Login_3, name='Login_3'),
    path('Logout/', Logout, name='Logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
