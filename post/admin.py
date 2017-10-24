# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone
from .models import Post, Competition
from django import forms


# Set validation errors for non consecutive dates and multiple competitions
class NewCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        exclude = (
            'winner', 'prize'
        )

    def clean(self):
        now = timezone.now()
        comp_list = Competition.objects.order_by('-vote_period_end')
        comp = comp_list[0]

        entry_start = self.cleaned_data.get('entry_period_start')
        entry_fin = self.cleaned_data.get('entry_period_fin')
        vote_start = self.cleaned_data.get('vote_period_start')
        vote_end = self.cleaned_data.get('vote_period_end')

        if now < entry_start:
            raise forms.ValidationError('Start date must be before now')
        if entry_fin < entry_start or vote_end < vote_start or vote_start < entry_fin:
            raise forms.ValidationError('Invalid dates')
        elif comp.is_active():
            raise forms.ValidationError('Only one active competition is permitted at a time')
        return self.cleaned_data


class CompetitionAdmin(admin.ModelAdmin):
    form = NewCompetitionForm
    list_display = (
        'title', 'brief', 'entry_period_start', 'vote_period_end', 'winner', 'prize',
    )


admin.site.register(Post)
admin.site.register(Competition, CompetitionAdmin)


