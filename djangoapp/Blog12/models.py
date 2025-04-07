from django.db import models
from utils.model_validators import random_letters,slugify_new,resize_image
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment
from django.shortcuts import render,reverse

# Create your models here.



class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
           self.name=self.file.name
        currente_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False
        if self.file:
            cover_change = currente_file_name != self.file.name
        if file_changed:
            resize_image(self.file, 900, True, 75)
        return super_save


class Tag(models.Model):

    class Meta:
        verbose_name='Tag'
        verbose_name_plural = "Tags"
    name=models.CharField(max_length=255)
    slug=models.SlugField(
        max_length=255,unique=True,
        default=None,null=True,blank=True
    )
    def __str__(self):
        return  self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify_new(self.name)
        return super().save(*args, **kwargs)

class Category(models.Model):
    class Meta:
        verbose_name='Category'
        verbose_name_plural = "Categories"
    name=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True,
        default=None,null=True,blank=True)

    def __str__(self):
        return  self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify_new(self.name)
        return super().save(*args, **kwargs)

class Page(models.Model):
    class Meta:
        verbose_name='Page'
        verbose_name_plural = "Pages"
    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255,unique=True,
        default=None,null=True,blank=True)
    is_published=models.BooleanField(default=False,help_text='este campo devera'
                                                               'estar marcado para a pagina'
                                                               'ser exibido publicamente')
    content=models.TextField(max_length=1500,blank=True,null=True)

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('Blog12:index')
        return reverse('Blog12:page',args=(self.slug,))
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify_new(self.title)
        return super().save(*args, **kwargs)
    def __str__(self):
        return  self.title


class PostManager(models.Manager):
    def get_published(self):
        return (self.
                filter(is_published=True).
                order_by('-pk')
                )

class Post(models.Model):
    class Meta:
        verbose_name='Post'
        verbose_name_plural = "Posts"
    objects = PostManager()#executar uma classe dentro de outra

    title=models.CharField(max_length=255)
    excerpt=models.TextField(max_length=1500,blank=True,null=True)
    slug=models.SlugField(max_length=255,unique=True,
        default=None,null=True,blank=True)
    is_published = models.BooleanField(default=False,help_text='este campo devera'
                                                               'estar marcado para o post'
                                                               'ser publicado')
    content=models.TextField(max_length=1500,blank=True,null=True)
    cover=models.ImageField(blank=True,null=True,upload_to="posts/%Y/%m/",)
    cover_in_post_contente=models.BooleanField(default=False,
    help_text=' Exibir a imagem de capa tambem dentro do conteudo do post?')
    created_at=models.DateTimeField(auto_now_add=True,)
    created_by=models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True,blank=True,
                                 related_name='page_created_by')
    updated_at=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='page_updated_by'
    )
    categories=models.ForeignKey(Category,blank=True,
                                 on_delete=models.SET_NULL,null=True,default=None)
    tags=models.ManyToManyField(Tag,blank=True,default='')
    

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('Blog12:index')
        return reverse('Blog12:post',args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify_new(self.title)
        currente_cover = str(self.cover.name)
        super_save=super().save(*args, **kwargs)
        cover_change=False
        if self.cover:
            cover_change=currente_cover!=self.cover.name
        if cover_change:
            resize_image(self.cover,900,True,75)
        return super_save






'''
    def save(self,*args,**kwargs):
        currente_favicon_name = str(self.favicon.name)
        super().save(*args,**kwargs)
        favicon_change = False
        if self.favicon:
            favicon_change=currente_favicon_name!=self.favicon.name
        if favicon_change:
            resize_image(self.favicon,32)


'''