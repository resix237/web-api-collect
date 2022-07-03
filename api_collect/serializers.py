from asyncore import write
from dataclasses import field
from importlib.metadata import requires
from . import models 
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class imageTagsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.images_tags    
        fields=['tags_value']

class tagsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.tags    
        fields="__all__"



class imageSerializer(WritableNestedModelSerializer):
    list_tags=imageTagsSerializer(many=True)
    class Meta:
        model=models.images
        fields=['id', 'link','count','his_tags','list_tags']
        #depth=1



class ImageModelSerializer(serializers.ModelSerializer):
    imagesLinks=serializers.ImageField(required=False)
    class Meta:
        model=models.imagesModel
        fields=['id', 'imagesLinks']