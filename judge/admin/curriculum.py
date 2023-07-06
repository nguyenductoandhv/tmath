from typing import Any, Optional
from django.contrib import admin
from django import forms
from django.db.models import Count

from judge.models import Curriculum, CurriculumContest, PublicProblem, Problem, Contest
from grappelli.forms import GrappelliSortableHiddenMixin


class CurriculumContestInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = CurriculumContest
    extra = 0
    autocomplete_fields = ["contest"]
    sortable_field_name = "order"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contest":
            kwargs["queryset"] = Contest.objects.filter(is_visible=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PublicProblemInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = PublicProblem
    extra = 0
    autocomplete_fields = ["problem"]
    sortable_field_name = "order"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "problem":
            kwargs["queryset"] = Problem.objects.annotate(case_count=Count('cases')).filter(case_count__gt=0, is_public=False).order_by('-pk')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = "__all__"


class CurriculumAdmin(admin.ModelAdmin):
    form = CurriculumForm
    list_display = ["name"]
    search_fields = ["name"]
    inlines = [CurriculumContestInline, PublicProblemInline]