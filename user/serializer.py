from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from drf_writable_nested import WritableNestedModelSerializer

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    # pour qu'un champ soit unique pour tout les users
    # validators=[UniqueValidator(queryset=User.objects.all())]
   # profile = UserProfileSerializer(source = 'userprofile__genre')
    # ce champs est un email et doit être unique parmis tout les users
    #email = serializers.EmailField( required=True)

   # en écriture seulement
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])
    #password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name')
        # validation extra
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    """
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    """

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        # pour qu'un user x ne modifie pas les coordonnées du user y
      #  user = self.context['request'].user
       # if user.pk != instance.pk:
        #    raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']

        instance.save()

        return instance


class RegisterSerializer(WritableNestedModelSerializer):
    """"
    avec cette méthode la mise à jour ne passe pas
    TODO: faudrait que le username soit le numéro de téléphone, je dois le renommer
    """
    donnee_utilisateur = UserCreateSerializer(source='user')

    class Meta:
        model = UserProfile
        fields = ('donnee_utilisateur', 'id', 'genre',
                  'date_naissance', 'affiliation', 'email')


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ForgetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])

    class Meta:
        model = User
        fields = ('password',)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        # validation extra
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    """
        def validate_username(self, value):
            user = self.context['request'].user
            if User.objects.exclude(pk=user.pk).filter(username=value).exists():
                raise serializers.ValidationError({"username": "This username is already in use."})
            return value
            """

    def update(self, instance, validated_data):
        # pour qu'un user x ne modifie pas les coordonnées du user y
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['image']

# sérialisation du token:revendication personnalise et pas compatible avec
# la liste noire. permet d'ajouter le username et son id au token


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token
