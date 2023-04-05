from django.db import models
from ckeditor.fields import RichTextField
import os, uuid


def get_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('food', filename)


class Category(models.Model):
    name_uz = models.CharField(max_length=150)
    name_ru = models.CharField(max_length=150)

    def __str__(self):
        return self.name_uz


class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food')
    name_uz = models.CharField(max_length=150)
    name_ru = models.CharField(max_length=150)
    description_uz = RichTextField()
    description_ru = RichTextField()
    search_variants = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name_uz


class FoodImages(models.Model):
    notification = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=get_image, null=True, blank=True)