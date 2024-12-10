from django.urls import path

from catalog import views

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('brands/<slug:brand_slug>', views.BrandView.as_view(), name='brand'),
    path('categories/<slug:category_slug>', views.CategoryView.as_view(), name='category'),
    path('<slug:brand_slug>/<slug:category_slug>', views.OfferView.as_view(), name='offer'),
    path('search/', views.SiteSearchView.as_view(), name='search_page'),
    path('brands-with-certificates/', views.BrandsWithCertificatesView.as_view(), name='brands_with_certificates'),
    path('brand/<int:pk>/certificates/', views.BrandCertificatesDetailView.as_view(), name='brand_certificates'),
    path('work/', views.WorkView.as_view(), name='work'),
    
    path('contact/', views.ContactFormView.as_view(), name='contact'),
]
