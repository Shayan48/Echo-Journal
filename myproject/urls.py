from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('blogs/', include('blog.urls', namespace='blogs')),  # ✅ Correct
    path('about/', views.aboutPage, name='about'),
    path('team/', views.teamPage, name='team'),
    path('contact/', views.ContactPage, name='contact'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', blog_views.signup, name='signup'),  # custom signup view
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)