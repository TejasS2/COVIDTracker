from django.urls import path

from . import views

app_name = "countries"

urlpatterns = [
   path("", views.home, name="home"),
   path("list", views.CountryViewList.as_view(), name="country_list"),
   path("list/<int:pk>", views.CountryDetailView.as_view(), name="country_detail"),
   path("list/<int:pk>/<str:date>", views.CountryDateDetailView.as_view(), name="country_date_detail"),
   path('add-user', views.UserCreateView.as_view(), name='add_user'),
   path('fetch-countries', views.fetch_countries, name='fetch_countries'),
   path('fetch-countries/<int:country_id>/', views.fetch_data, name='fetch_data'),
   path("info", views.info, name="info"),
]
