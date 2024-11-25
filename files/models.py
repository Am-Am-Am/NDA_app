from django.db import models
from django.utils.safestring import mark_safe

from catalog.models import Category


class ModelImage(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='category/images', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Изображения'

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'

    def __str__(self):
        return self.image.url


class ModelFile(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to='category/certificates', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.file.url
