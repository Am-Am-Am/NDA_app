from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib import messages

from catalog.models import Category, Brand, Offer
from files.models import ModelFile, ModelImage
from cart.forms import CartAddProductForm
from django.views.generic import DetailView

SEARCH_QUERY_PARAM = 'q'


def breadcrumbs_path(category):
    parents = category.parents.prefetch_related('parents').select_related('brand').all()
    breadcrumbs = []
    while len(parents) > 0:
        parents_path = [parent for parent in parents if parent.brand is not None]
        if parents_path:
            if len(parents_path) > 1:
                raise ValueError('We don\'t expect multiple brand parents')
            if len(parents_path) == 1:
                breadcrumbs.insert(0, parents_path[0])
            parents = parents_path[0].parents.all()
        else:
            parents_path = [parent for parent in parents if parent.brand is None]
            if len(parents_path) > 1:
                raise ValueError('We don\'t expect multiple brand parents')
            if len(parents_path) == 1:
                breadcrumbs.insert(0, parents_path[0])
            parents = parents_path[0].parents.all()
    return breadcrumbs


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.visible.all().order_by('name')
        context['categories'] = Category.visible.filter(parents=None)
        # context['categories'] = Category.visible.filter(parents=None).filter(brand=None)
        return context


class CategoryView(TemplateView):
    model = Category
    template_name = 'catalog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.visible.select_related('brand').get(slug=self.kwargs['category_slug'])
        context['brand'] = category.brand
        context['category'] = category
        context['breadcrumbs'] = breadcrumbs_path(category)
        return context


class BrandView(TemplateView):
    model = Category
    template_name = 'catalog/brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = get_object_or_404(Brand.visible, slug=self.kwargs['brand_slug'])
        context['categories'] = Category.visible.filter(parents=None, brand=brand).select_related('brand')
        context['brand'] = brand
        return context


class OfferView(TemplateView):
    model = Offer
    template_name = 'catalog/offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.visible.select_related('brand').get(slug=self.kwargs['category_slug'])
        context['category'] = category
        context['brand'] = category.brand
        context['offers'] = Offer.visible.filter(category=category.id)
        context['images'] = ModelImage.objects.filter(category=category.id)
        context['certificates'] = ModelFile.objects.filter(category=category.id)
        context['breadcrumbs'] = breadcrumbs_path(category)
        context['cart_product_form'] = CartAddProductForm()
        return context


class SiteSearchView(ListView):
    model = Category
    template_name = 'catalog/components/search.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get(SEARCH_QUERY_PARAM, '')
        qs = super().get_queryset()
        if len(query) < 3:
            messages.error(self.request, message='Слишком короткий запрос. Попробуйте увеличить количество символов в запросе')
            return qs.none()

        related_offers = Prefetch(
            'offer',
            queryset=Offer.visible.filter(name__icontains=query) or Offer.visible.filter(description__icontains=query),
            to_attr='related_offers')
        qs = (
            qs.filter(is_final=True).filter(Q(name__icontains=query) | Q(offer__name__icontains=query) | Q(offer__description__icontains=query))
            .prefetch_related(related_offers).distinct()
        )
        return qs

class BrandsWithCertificatesView(ListView):
    model = Brand
    template_name = 'catalog/certificates.html'  
    context_object_name = 'brands'

    def get_queryset(self):
        queryset = super().get_queryset()
        brands_with_certs = set(Brand.objects.filter(category__modelfile__isnull=False))
        return queryset.filter(id__in=[b.id for b in brands_with_certs])
    

class BrandCertificatesDetailView(DetailView):
    model = Brand
    template_name = 'catalog/brand_certificates_detail.html'  # Указать путь к шаблону
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.object
        certificates = ModelFile.objects.filter(category__brand=brand)
        context['certificates'] = certificates
        return context
    
class WorkView(TemplateView):
    template_name = 'catalog/work.html'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'