from django import forms

from .models import Review, RatingStar, Rating


class ReviewForm(forms.ModelForm):
	'''Форма комментария/отзыва'''
	class Meta:
		model = Review
		fields = ('text', 'email', 'name')

class RatingForm(forms.ModelForm):
	'''Форма добаления рейтинга'''
	star = forms.ModelChoiceField(
		queryset=RatingStar.objects.all(),
		widget=forms.RadioSelect(),
		empty_label=None
		)

	class Meta:
		model = Rating
		fields = ('star', )

class MyForm(forms.Form):
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)