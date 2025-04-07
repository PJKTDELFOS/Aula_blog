from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id','name','slug'
    list_display_links = 'id','name','slug'
    search_fields = 'name','slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug'
    list_display_links = 'id', 'name', 'slug'
    search_fields = 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',)

    }
#o summernote usa no admin
@admin.register(models.Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }


#importar o summernote, e importar para  o postadmin
@admin.register(models.Post)
class Postadmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'slug','is_published','created_by'
    list_display_links = 'title',
    search_fields = 'title','id','excerpt','content','cover'
    list_per_page = 50
    ordering = '-id',
    list_editable = ('is_published',)
    list_filter = 'categories','is_published',
    readonly_fields = 'created_at','updated_at','created_by','updated_by','link'
    prepopulated_fields = {
        'slug': ('title',)
    }
    autocomplete_fields = 'tags', 'categories'

    def link(self,obj):
        if not obj.pk:
            return ''
        url_do_post = reverse('Blog12:post', args=(obj.slug,))
        safer_url = mark_safe(f'<a target ="_blank"  href="{url_do_post}">Ver Post </a>')
        return safer_url
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()




