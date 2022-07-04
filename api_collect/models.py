from django.db import models



# Create your models here.

class tags(models.Model):
    name= models.CharField(max_length=200)
    
    def __str__(self):
         return self.name


class images_tags(models.Model):
    tags_value=models.ForeignKey(tags,on_delete=models.RESTRICT)

class images(models.Model):
    link=models.CharField(max_length=200)
    count=models.IntegerField(null=True)
    his_tags=models.ForeignKey(tags,on_delete=models.RESTRICT,null=True)
    list_tags=models.ManyToManyField(images_tags)
class imagesReconnu(models.Model):
    link=models.CharField(max_length=200)
    pourcentage=models.IntegerField(null=True)
    his_tags=models.ForeignKey(tags,on_delete=models.RESTRICT,null=True)
class imagesModel(models.Model):
    imagesLinks= models.ImageField(upload_to="images/")
    his_tags=models.CharField(max_length=200, blank=True)
    


