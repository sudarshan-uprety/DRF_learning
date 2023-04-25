from rest_framework import serializers
from .models import User,Post,PostVote
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

    class Meta:
        model=User
        fields=['email','name','phone','address','created_at']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    password2=serializers.CharField()

    class Meta:
        model = User  # add this line
        fields = ['password','password2']

    def create(self, validated_data):
        password=validated_data['password']
        password2=validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError("Password do not match.")
        email=self.context['request'].user.email
        user=User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return user

class VoteSerializer(serializers.ModelSerializer):
    vote=serializers.IntegerField()

    class Meta:
        model = PostVote
        fields=['vote']

    def create(self,validated_data):
        post=Post.objects.get(id=validated_data['pk'])
        email=User.objects.get(email=validated_data['email'])
        vote=PostVote.objects.create(
            post=post,email=email,rating=validated_data['vote']
        )
        vote.save()
        return vote
