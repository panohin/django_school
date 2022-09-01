from django.contrib import admin

from . import models


admin.site.register(models.Category)
admin.site.register(models.Actor)
admin.site.register(models.Genre)
admin.site.register(models.RatingStar)
admin.site.register(models.Rating)
admin.site.register(models.Review)

admin.site.register(models.Movie)
admin.site.register(models.MovieShot)