from rest_framework import serializers
from .models import User,Post
from rest_framework.validators import UniqueValidator
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['name','email','phone','address','password','password2','is_staff','is_superuser']


    def create(self,validated_date):
        user=User.objects.create(
            name=validated_date['name'],email=validated_date['email'],
        )
        user.set_password(validated_date['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password']



class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(write_only=True, default=timezone.now)
    updated_at = serializers.DateTimeField(write_only=True, default=timezone.now)

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        post = Post.objects.create(
            email=self.context['request'].user,
            title=validated_data['title'],
            content=validated_data['content']
        )
        post.save()
        return post
    
class ProfileViewSerializer(serializers.ModelSerializer):
    password=serializers.CharField()
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email','name','phone','created_at','password','password2']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField()
    class Meta:
        model=User
        fields=['password','password2']
    
    def validate(self,data):
        user=self.context.get('user')
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password do not match")
        user.set_password(data['password'])
        user.save()
        return data
