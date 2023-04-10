from django.contrib import admin
from .models import  User, branch_school, Listing, Img, Rating
# Register your models here.

admin.site.register(User)
admin.site.register(branch_school)
admin.site.register(Listing)
admin.site.register(Img)
admin.site.register(Rating)