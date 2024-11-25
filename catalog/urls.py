from django.urls import path

from catalog import views

urlpatterns = [
    path('brands/<slug:brand_slug>', views.BrandView.as_view(), name='brand'),
    path('categories/<slug:category_slug>', views.CategoryView.as_view(), name='category'),
    path('<slug:brand_slug>/<slug:category_slug>', views.OfferView.as_view(), name='offer'),
    path('search/', views.SiteSearchView.as_view(), name='search_page'),
]
