
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializer import RegisterSerializer, ChangePasswordSerializer, MyTokenObtainPairSerializer, UpdateUserProfileSerializer, UserUpdateSerializer, ForgetPasswordSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import UserProfile
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
import json
# déconnection
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

import random

"""
TODO: il va falloir gérer la notion d'authentification, définir des code de réponse personalisés. avec des status,et message d'erreurs,gérer des exceptions rest
"""

# vue de création
# FIXME: lorsqu'un user existe déjà il faudra être à mesure de retourner une réponse qui permet à la vue de savoir cela plutôt qu'une exception
# savoir capturer les erreurs pour retourner un msg personalisé
# pour créer un utilisateur. quelques fois ça bugg bad request. pourtant le json envoyé est correct


class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# vue pour changer le mot de passe


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

# vue pour modifier le mot de passe dans la mesure ou le user l'a oublié.donc ne nécessite pas une authentification


class ForgetPasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordSerializer

# recherche un user en sachant son id


@api_view(['GET'])
def get_userid(request, pk):
    user = User.objects.get(pk=pk)
    if (not user):
        status = 404
        objet = {}
        return Response(objet)
    else:
        userprofile = UserProfile.objects.filter(user=user)
        if userprofile:
            status = 200
            objet = {
                'nom': user.first_name,
                'prenom': user.last_name,
                'genre': userprofile[0].genre,
                'tel': user.username
            }
            print(objet)
        return Response(objet)

# recherche un user en utilisant son username, utiliser pour le mot de passe oublié


@api_view(['GET'])
def get_user(request, username):
    user = User.objects.get(username=username)
    if (not user):
        status = 404
        return Response({"message": "not found"})
    else:
        userprofile = UserProfile.objects.filter(user=user)
        status = 200
        objet = {
            'firstName': user.first_name,
            'id': user.pk,
            'username': user.username
        }
        return Response(objet)
# TODO: fonction exploiter pour le code

# non utilisée, fonction pour la génération du code secret


def generatedcode(request):
    code = random.randint(10000, 99999)

# vu pour le login


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         resultat = {
    #             "data": serializer.validated_data,
    #             "status": 200
    #         }
    #         return Response(resultat, status=status.HTTP_200_OK)
    #     else:
    #         resultat = {
    #             "data": {},
    #             "status": 401
    #         }
    #         return Response(resultat, status=status.HTTP_200_OK)


# pour modifier les information d'un user
class UpdateUserView(generics.UpdateAPIView):

    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

# pour modifier l'image de profil ou tout autre information relative à un user


class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateUserProfileSerializer
    permission_classes = (IsAuthenticated,)

# vue pour la deconnexion


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# non implémenté, pour récupérer le profil d'un utilisateur


@api_view(['GET'])
def GetUserProfile(request):

    userprofile = UserProfile.objects.all()
    # serialisons cet objet
    serialization = RegisterSerializer(userprofile, many=True)
    permission_classes = (IsAuthenticated,)
    return Response(serialization.data)

# pour récupérer le user courant


@api_view(['GET'])
def current_user(request):
    user = request.user

    profile = get_object_or_404(Profile, user=user)

    Profile_serializer = ProfileSerializer(profile)

    return Response(Profile_serializer.data)
