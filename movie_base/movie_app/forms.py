from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
	'''Форма комментария/отзыва'''
	class Meta:
		model = Review
		fields = ('text', 'email', 'name')