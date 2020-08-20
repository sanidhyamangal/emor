from django.contrib import admin
from .models import (User, Education, Experience, ProfileSkills, UserProject,
                     PriceAvailablity, Notification)

from .forms import UserForm
from django.contrib.auth.hashers import make_password

# Register your models here.
models_to_register = [
    Education, Experience, ProfileSkills, UserProject, PriceAvailablity,
    Notification
]

for model in models_to_register:
    admin.site.register(model)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    exclude = (
        'uid',
        'user_permissions',
    )

    def save_model(self, request, obj, form, change):
        if change:
            creds = User.objects.filter(pk=obj.pk).values()[0]
            if not obj.password:
                obj.password = creds['password']
            elif obj.password != creds['password']:
                obj.password = make_password(obj.password)
        else:
            obj.password = make_password(obj.password)
        obj.save()

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request)