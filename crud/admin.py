from django.contrib import admin
from .models import User,Post
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_superuser', 'is_active']
    fieldsets=(
        ('User Credentials',{'fields':('email','password')}),
        ('Personal info',{'fields':('name',)}),
        ('Permissions',{'fields':('is_superuser',)})
    )
    add_fieldsets=(
        (None,{
        'classes':('wide',),
        'fields':('email','name','phone','address','password1','password2')
        }),
    )

class PostAdmin(admin.ModelAdmin):
    list_display=['email','title','content','created_at','updated_at']


admin.site.register(User,UserAdmin)
admin.site.register(Post,PostAdmin)