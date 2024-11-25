from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.urls import reverse

from tinymce.widgets import TinyMCE

from catalog.models import Brand, Category, Offer
from files.models import ModelImage, ModelFile
from catalog.admin_filters import DropdownFilter, RelatedOnlyDropdownFilter, CategoryRelatedOnlyDropdownFilter


"""Общие методы админки"""


class MyAdminSite(AdminSite):
    def get_app_list(self, request, app_label=None):
        """Возвращает отсортированный список зарегистрированных приложений"""
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


admin.site = MyAdminSite()

admin.site.empty_value_display = '---- ОТСУТСТВУЕТ'


class OfferInline(admin.TabularInline):
    model = Offer
    can_delete = True
    extra = 0
    show_change_link = True
    classes = ['collapse', 'wide']


class CategoryImageInline(admin.TabularInline):
    model = ModelImage
    readonly_fields = ('image_preview',)


class CategoryFileInline(admin.TabularInline):
    model = ModelFile


""""Классы админки"""


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'place',
        'status',
        'banner_color'
    )
    list_editable = ('place', 'slug', 'status', 'banner_color')
    list_filter = (('name', DropdownFilter), 'status')
    fields = [
        'name',
        'description',
        'slug',
        'place',
        'status',
        'logo',
        'banner',
        'banner_color'
    ]
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ['brand']
    list_display = (
        'name',
        'brand',
        'slug',
        'place',
        'status',
        'is_final'
    )
    list_editable = ('place', 'slug', 'status')
    list_filter = (
        ('brand', RelatedOnlyDropdownFilter),
        ('parents', CategoryRelatedOnlyDropdownFilter),
        'status',
        'is_final'
    )
    fields = [
        'name',
        'description',
        'logo',
        'banner',
        'instruction',
        'parents',
        'brand',
        'slug',
        'place',
        'status',
        'is_final'
    ]
    filter_horizontal = ('parents', )
    autocomplete_fields = ('brand', )
    inlines = [OfferInline, CategoryImageInline, CategoryFileInline]
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'description':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        qs = form.base_fields['parents'].queryset
        form.base_fields['parents'].queryset = qs.select_related('brand').all()
        return form


class OfferAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'brand_name',
        'category',
        'place',
        'status'
    )
    list_editable = ('place', 'status')
    list_filter = (
        ('category__brand', RelatedOnlyDropdownFilter),
        ('category', CategoryRelatedOnlyDropdownFilter),
        'status'
    )
    fields = [
        'name',
        'description',
        'shipping_pack'
        'tech_info',
        'ctru',
        'category',
        'place',
        'status'
    ]
    autocomplete_fields = ['category']
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'category__brand')

    @admin.display(description='Бренд', ordering='name')
    def brand_name(self, obj):
        return obj.category.brand.name


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
