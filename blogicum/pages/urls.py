from django.urls import path

from pages import views


app_name = "pages"

urlpatterns = [
    path("about/", views.AboutView.as_view(), name="about"),
    path("rules/", views.RulesView.as_view(), name="rules"),
]


handler403 = 'pages.views.custom_403'
handler404 = 'pages.views.custom_404'
handler500 = 'pages.views.custom_500'