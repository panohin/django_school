from django.contrib import admin

from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'url')
	list_display_links = ('name',)

class ReviewInline(admin.TabularInline):
	model = models.Review
	extra = 1
	readonly_fields = ('name', 'email')

@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url', 'draft')
	list_filter = ('category', 'year')
	search_fields = ('title', 'category__name')
	inlines = [ReviewInline]
	save_on_top = True
	save_as = True
	list_editable = ('draft',)
	# fields = (('actors', 'directors', 'genres'),)
	# fieldsets = {
	# ('Title', {
	# 	'fields' : (('title', 'tagline'),)
	# 	})
	# }

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'parent', 'movie', 'id')
	readonly_fields = ('name', 'email')


# admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Actor)
admin.site.register(models.Genre)
admin.site.register(models.RatingStar)
admin.site.register(models.Rating)
# admin.site.register(models.Review)
# admin.site.register(models.Movie)
admin.site.register(models.MovieShot)