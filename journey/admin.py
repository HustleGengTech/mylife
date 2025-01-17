from django.contrib import admin
from django.contrib.auth.models import Group, User
from.models import Document,Profile,EmergencyContact,DocumentImage,Feedback
# Register your models here.
admin.site.register(Document)
admin.site.register(Profile)
admin.site.register(EmergencyContact)
admin.site.register(DocumentImage)
admin.site.register(Feedback)

#admin.site.register(Profile)

# #unregister
# admin.site.unregister(Group)

# #extend user model
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     fields = ['username']


# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)
# admin.site.register(Profile)

