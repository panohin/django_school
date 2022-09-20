from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from . import models


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = models.Movie
        fields = '__all__'

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
	list_display = ('title', 'category', 'url', 'draft', 'get_poster')
	list_filter = ('category', 'year')
	search_fields = ('title', 'category__name')
	inlines = [ReviewInline]
	save_on_top = True
	save_as = True
	list_editable = ('draft',)
	form = MovieAdminForm
	actions = ['publish', 'unpublish']

	# fields = (('actors', 'directors', 'genres'),)
	# fieldsets = {
	# ('Title', {
	# 	'fields' : (('title', 'tagline'),)
	# 	})
	# }

	def get_poster(self, obj):
		return mark_safe(f'<img src={obj.poster.url} width="60" heigth="40">')

	def unpublish(self, request, queryset):
		'''Снять с публикации'''
		row_update = queryset.update(draft=True)
		if row_update == 1:
			message_bit = '1 запись обновлена'
		else:
			message_bit = f'{row_update} записей обновлено'
		self.message_user(request, message_bit)
	
	def publish(self, request, queryset):
		'''Опубликовать'''
		row_update = queryset.update(draft=False)
		if row_update == 1:
			message_bit = '1 запись обновлена'
		else:
			message_bit = f'{row_update} записей обновлено'
		self.message_user(request, message_bit)

	publish.short_description = 'Опубликовать'
	publish.allowed_permissions = ('change',)
	unpublish.short_description = 'Снять с публикации'
	unpublish.allowed_permissions = ('change',)
	
	get_poster.short_description = 'Постер'

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'parent', 'movie', 'id')
	readonly_fields = ('name', 'email')

@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
	list_display = ('name', 'age', 'get_image')

	def get_image(self, obj):
		return mark_safe(f'<img src={obj.image.url} width="30" heigth="40">')


# admin.site.register(models.Category, CategoryAdmin)
# admin.site.register(models.Actor)
admin.site.register(models.Genre)
admin.site.register(models.RatingStar)
admin.site.register(models.Rating)
# admin.site.register(models.Review)
# admin.site.register(models.Movie)
admin.site.register(models.MovieShot)