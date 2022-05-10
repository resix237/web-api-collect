from django.contrib import admin
from . import models

admin.site.register(models.images)
admin.site.register(models.images_tags)
admin.site.register(models.tags)
admin.site.register(models.imagesModel)

# Register your models here.
