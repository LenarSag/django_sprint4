from django.urls import path

from pages import views


app_name = "pages"

urlpatterns = [
    path("about/", views.AboutView.as_view(), name="about"),
    path("rules/", views.RulesView.as_view(), name="rules"),
]


handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.internal_server_error'
