
from itertools import count
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view
from webCollectSite.settings import BASE_DIR, CSV_FILE, MODEL_ML
from . import models
from . import serializers
import pandas as pd
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
import pickle
from sklearn.datasets import load_sample_image
from rest_framework.parsers import MultiPartParser, FormParser
import numpy as np
import os 
# Create your views here.

#importation de la parti data sscience
from keras.preprocessing import image
import keras
from keras.applications.vgg19 import preprocess_input
class imagesView(viewsets.ModelViewSet):
   
    serializer_class= serializers.imageSerializer

    def get_queryset(self):
        return models.images.objects.all().filter(count__lte=2)#count__lte


class tagsView(viewsets.ModelViewSet):
    queryset=models.tags.objects.all()
    serializer_class= serializers.tagsSerializer




def chragerImageBd(request):
    df = pd.read_csv(CSV_FILE)   
    urls = df['PID_URLS']
    for url in urls:
        models.images.objects.create(link=url, count=0)
    return render(request,'Ack.html')   









# class imagesList(generics.ListCreateAPIView):
#     queryset = models.images.objects.all().filter(count__lte=3)
#     serializer_class = serializers.imageSerializer
# class imagesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.images.objects.all().filter(count__lte=3)
#     serializer_class = serializers.imageSerializer



class imageApiView(APIView):
    parser_classes=[MultiPartParser, FormParser]
    

    def post(self,request, format=None):
        print(request.data)
        serializer=serializers.ImageModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            lesClasses = ['Bamileke', 'Beti', 'Bamenda', 'Douala', 'Peulh']
            cnn = keras.models.load_model(MODEL_ML)
            img_path=os.path.join(BASE_DIR/'media/images', serializer.data['imagesLinks'].split('/')[-1])

            img = image.load_img(img_path, target_size=(224,224))
        
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            predictions=cnn.predict(x)
            taux = np.amax(predictions)*100
            serializer.his_tags=lesClasses[np.argmax(predictions)]
            #fin de prediction 
            #je vais creer un objet image pour renvoyer la serialization

            imageTampon=models.imagesReconnu(link=serializer.data['imagesLinks'])
            tags=models.tags.objects.get(name=lesClasses[np.argmax(predictions)])
            imageTampon.his_tags=tags
            imageTampon.pourcentage=np.max(predictions)*100
            imageTampon.save()
            serializer2=serializers.imageReconnuSerializer(imageTampon)

            print(lesClasses[np.argmax(predictions)])
        
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class imageViewModel(viewsets.ModelViewSet):
    queryset =models.imagesModel.objects.all()
    serializer_class = serializers.ImageModelSerializer
    parser_classes = [MultiPartParser, FormParser]
   
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
       
        lesClasses = ['Bamileke', 'Beti', 'Bamenda', 'Douala', 'Peulh']
        cnn = keras.models.load_model(MODEL_ML)
        img_path=os.path.join(BASE_DIR/'media/images', serializer.data['imagesLinks'].split('/')[-1])

        img = image.load_img(img_path, target_size=(224,224))
        
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        predictions=cnn.predict(x)
        taux = np.amax(predictions)*100
        serializer.his_tags=lesClasses[np.argmax(predictions)]
        #fin de prediction 
        #je vais creer un objet image pour renvoyer la serialization

        imageTampon=models.imagesReconnu(link=serializer.data['imagesLinks'])
        tags=models.tags.objects.get(name=lesClasses[np.argmax(predictions)])
        imageTampon.his_tags=tags
        imageTampon.pourcentage=np.max(predictions)*100
        imageTampon.save()
        serializer2=serializers.imageReconnuSerializer(imageTampon)

        print(lesClasses[np.argmax(predictions)])
        
        headers = self.get_success_headers(serializer2.data)
        return Response(serializer2.data, status=status.HTTP_201_CREATED, headers=headers)

    # def post(self, request, *args, **kwargs):

    #     monSerializer = serializers.ImageModelSerializer(data=request.data)
    #     if monSerializer.is_valid():
            
            

    #         monSerializer.his_tags=lesClasses[np.argmax(predictions)]
    #         monSerializer.save()


    #         return Response(data=monSerializer.data, status=status.HTTP_201_CREATED)
    #     return Response(monSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class imageModelViewSet(viewsets.ModelViewSet):
    queryset =models.imagesModel.objects.all()
    serializer_class = serializers.ImageModelSerializer
    parser_classes = (MultiPartParser, FormParser)
   



""" cnn = keras.models.load_model('AfricultoCNN.h5')

#model = pickle.load(open("model.pkl", "rb"))

lesClasses = ['Bamileke', 'Beti', 'Bamenda', 'Douala', 'Peulh']
img_path = '/content/drive/MyDrive/cnn_datasets/test.jpg'
img = image.load_img(img_path, target_size=(224,224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
predictions=model.predict(x)
print( 'PROBABILITES : %s' %predictions)
taux = np.amax(predictions)*100
print('PEUPLE : '+lesClasses[np.argmax(predictions)]+' (avec un taux de %.2f' %taux +'%)\n')
 """