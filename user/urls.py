
from user.views import RegisterView, ChangePasswordView, GetUserProfile, UpdateUserView, UpdateUserProfileView, ForgetPasswordView, get_userid, get_user, MyTokenObtainPairView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

"""
TODO: ajouter les vues dans le fichier views.py
puis corriger les routes
"""

"""
Lorsque le modele hérite de viewset.Viewsets on doit renseigner dans
l'urls au niveau de register. register le basename
avec les modelsviewset cela est implicite.
"""


urlpatterns = [
    # pour se connecter
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # avec  body:refresh pour actualiser l'accès
    path('loginrefresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # pour s'enregistrer
    path('register/', RegisterView.as_view(), name="user_register"),
    # modifier le mot de passe
    path(
        'change_password/<int:pk>/',
        ChangePasswordView.as_view(),
        name='auth_change_password'),
    # changer de mot de passe sans être connecté
    path(
        'forget_password/<int:pk>/',
        ForgetPasswordView.as_view(),
        name='auth_forget_password'),
    # vue pour récupérer le user sachant sont id
    path('get_userid/<int:pk>/', get_userid, name="get_user"),
    # vue pour récupérer le user sachant son username
    path('get_user/<str:username>/', get_user, name="get_user"),
    #
    path('all_user/', GetUserProfile, name="user_register"),
    # mise à jour du profile,cela se fait en deux temps pour le user puis le
    # userprofile
    path(
        'update_user/<int:pk>/',
        UpdateUserView.as_view(),
        name='update_user'),
    path(
        'update_profile/<int:pk>/',
        UpdateUserProfileView.as_view(),
        name="update_profile"),
    # path('logout/', LogoutView.as_view(), name='auth_logout'),

]
