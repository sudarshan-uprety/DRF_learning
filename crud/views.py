from django.shortcuts import render,get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate

from .models import Post,User,PostVote

from django.contrib.auth import get_user

from .serializers import UserSerializer,PostSerializer,LoginSerializer,ProfileViewSerializer,ChangePasswordSerializer,VoteSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import Avg,Count



#Generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class RegisterView(generics.GenericAPIView):

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password=serializer.validated_data['password']
        password2=serializer.validated_data['password2']
        if password!=password2:
            return Response({"error":"passsword and confirm password do not match"})
        validated_data=serializer.validated_data
        validated_data.pop('password2')
        user=User(**validated_data)
        user.set_password(password)
        user.is_active=True
        user.save()
        return Response({"ststus":"User registered successfully"},status=201)


    

class LoginView(generics.GenericAPIView):

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({"token":token,"success":"User loggedin successfully"},status=200)
            else:
                return Response({"error":{"No user found":['Email or password is not valid']}},status=400)
        else:
            return Response(serializer.errors,status=403)



class PostView(generics.GenericAPIView):

    permission_classes=[IsAuthenticated]


    def post(self,request):
        # user=request.user
        serializer=PostSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        post=serializer.create(validated_data)
        return Response({"success":"User post created"} ,status=200)


    def put(self,request,pk):
        try:
            post=Post.objects.get(id=pk,email=request.user.email)
            serializer=PostSerializer(post,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
                return Response({"error":"post not found or you're not authorized "},status=403)

    
    def get(self,request):
        posts=Post.objects.filter(email=request.user.email).values('title','content','created_at')
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
        
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk, email=request.user.email)
            post.delete()
            return Response({"message": "Post deleted successfully."}, status=204)
        except ObjectDoesNotExist:
            return Response({"error": "Post not found or you are not authorized to delete it."}, status=404)


class UserProfileView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=ProfileViewSerializer(request.user)
        return Response(serializer.data,status=200)
    


class ChangePasswordView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success":"Password changed successfully"})
    


class VotePostView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,pk):
        serializer=VoteSerializer(data=request.data,context={"request":request.user})
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        validated_data['email']=request.user.email
        validated_data['pk']=pk
        post=Post.objects.get(id=pk)
        if not post:
            return Response({"error":"Sorry post do not exist"})
        post_already=PostVote.objects.get(email=request.user.email,post_id=pk)
        if post_already:
            return Response({"error":"Sorry you already voted in this post"})
        serializer.save()
        return Response({"success":"Voted successfully"})



class PostView(generics.GenericAPIView):

    def get_client_ip(self,request):
        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
        print(x_forwarded_for)
        if x_forwarded_for:
            ip=x_forwarded_for.split(',')[-1].strip()
        else:
            ip=request.META.get('REMOTE_ADDR')
        return ip
    
    def get(self,request,pk):
        post=Post.objects.filter(id=pk).select_related('email').values('title','content','email','created_at')
        if post:
            self.get_client_ip(request)
        return Response({"success":"Data","post_details":post})



class ReviewPostView(generics.GenericAPIView):

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            print(post)
        except Post.DoesNotExist:
            return Response({"error": "Sorry we do not have that post."}, status=status.HTTP_404_NOT_FOUND)

        post_votes = PostVote.objects.filter(post=post)
        if post_votes:
            ip = self.get_client_ip(request)
            print(ip)
            average_rating = post_votes.aggregate(Avg('rating'))['rating__avg']
            views_count = post.views.count()
            return Response({"average_rating": average_rating, "views_count": views_count})
        else:
            return Response({"error": "Sorry we do not have any votes for that post."}, status=status.HTTP_404_NOT_FOUND)