from distutils.command.upload import upload
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.urls import reverse

# Create your models here.


def get_img_upload_path(instance, filename):
    return f'{instance.name}/images/{filename}'

class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug= models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255,blank=True)
    cat_img = models.ImageField(upload_to='get_img_upload_path',blank=True)
    

    class Meta:
        verbose_name = "category"
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    def __str__(self):
        return self.category_name


  