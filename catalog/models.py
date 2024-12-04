from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_save
from django.dispatch import receiver

from NDA_app.settings import PRIVATE_ROOT, SENDFILE_ROOT


private_storage = FileSystemStorage(location=PRIVATE_ROOT + SENDFILE_ROOT, base_url='/files')


"""Общие классы и миксины"""


class NotHidden(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PUBLISHED')


class BaseFields(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        PUBLISHED = 'PUBLISHED', 'Активен'
        ARCHIVED = 'ARCHIVED', 'В архиве'

    description = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    place = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Место в списке'
    )
    status = models.CharField(
        max_length=128,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус показа на страницах'
    )

    objects = models.Manager()
    visible = NotHidden()

    class Meta:
        abstract = True


"""Модели"""


class Brand(BaseFields):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Бренд',
        null=True,
        )
    logo = models.ImageField(
        upload_to='brand/logo',
        default='',
        blank=True,
        verbose_name='Логотип бренда'
    )
    banner = models.ImageField(
        upload_to='brand/banner',
        default='',
        blank=True,
        verbose_name='Баннер бренда',
    )
    banner_color = models.CharField(
        max_length=32,
        default='#3391c5',
        null=True,
        verbose_name='Цвет баннера бренда'
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        verbose_name='url-адрес'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def save(self, *args, **kwargs):
        if not self.slug:  # если slug не задан, автоматически создаем его
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # вызываем метод родительского класса    

    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug': self.slug})

    def __str__(self):
        return self.name.upper()


class Category(BaseFields):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        null=True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд, к которому относится категория'
    )
    parents = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Родительские категории',
        related_name='children',
        symmetrical=False
    )
    logo = models.ImageField(
        upload_to='category/logo',
        default='',
        null=True,
        blank=True,
        verbose_name='Логотип категории'
    )
    banner = models.ImageField(
        upload_to='category/banner',
        default='',
        blank=True,
        verbose_name='Баннер категории'
    )
    instruction = models.FileField(
        storage=private_storage,
        upload_to='instructions',
        null=True,
        blank=True,
        verbose_name='Инструкция'
    )
    slug = models.SlugField(
        unique=True,
        max_length=128,
        db_index=True,
        verbose_name='url-адрес'
    )
    is_final = models.BooleanField(
        default=False,
        verbose_name='Отметка о том, что категория является финальной и в ней содержатся товары'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        if self.brand:
            return str(self.brand).upper() + '----' + self.name.upper()
        return 'ПОДБОРКА' + '----' + self.name.upper()


class Offer(BaseFields):
    name = models.CharField(
        max_length=128,
        verbose_name='Артикул'
    )
    shipping_pack = models.CharField(
        max_length=10,
        verbose_name="Количество в упаковке",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offer',
        verbose_name='Категория, к которой принадлежит товар'
    )
    tech_info = models.FileField(
        upload_to='files/instructions',
        null=True,
        blank=True,
        verbose_name='Техзадание'
    )
    ctru = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='КТРУ'
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Бренд',
        related_name='offers'
    )

    class Meta:
        ordering = ['place']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=Offer)
def set_brand_from_category(sender, instance, **kwargs):
    if instance.category and not instance.brand:
        instance.brand = instance.category.brand