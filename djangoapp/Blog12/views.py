from django.core.paginator import Paginator
from django.shortcuts import render,reverse,redirect
from django.urls import reverse_lazy
from typing import Any, Optional, Union
from Blog12.models import Post,Page
from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from django.http import Http404,HttpRequest,HttpResponse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView

posts = list(range(900))
itens_por_pagina=2

class Postlistview(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = ['-pk']
    paginate_by = itens_por_pagina
    queryset = Post.objects.get_published()

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context=super().get_context_data(**kwargs)
        context.update(
            {'page_title': 'Home - ',}
        )
        return context


class CreatedbyListvView(Postlistview):
    def __init__(self, **kwargs:Any) -> None:
        super().__init__(**kwargs)
        self._temp_context:dict[str,Any]={}

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        ctx=super().get_context_data(**kwargs)
        user=self._temp_context['user']
        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Postos de ' + user_full_name + ' -'

        ctx.update(
            {'page_title': page_title,}
        )
        return ctx

    def get_queryset(self)->QuerySet[Any]:
        qs=super().get_queryset()
        qs=qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs


    def get(self, request:HttpRequest, *args:Any, **kwargs:Any) -> HttpResponse:
        author_pk = self.kwargs['author_pk']
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            return redirect('Blog12:index')
        self._temp_context.update({
            'author_pk':author_pk,
            'user':user,
        })
        return super().get(request, *args, **kwargs)


class CategoryListvView(Postlistview):

    allow_empty = False

    def get_queryset(self)-> QuerySet[Any]:
        return super().get_queryset().filter(categories__slug=self.kwargs.get('slug'))


    def get_context_data(self,**kwargs):
        ctx=super().get_context_data(**kwargs)
        categoria=self.object_list[0].categories.name
        category_title='Posts de categoria ' + categoria + ' -'

        ctx.update(
            {'page_title': category_title,}
        )
        return ctx


class TagListvView(Postlistview):
    allow_empty = False

    def get_queryset(self)-> QuerySet[Any]:
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self,**kwargs):
        ctx=super().get_context_data(**kwargs)

        tag_title= f"{self.kwargs.get('slug')} - Tag - "

        ctx.update(
            {'page_title': tag_title,}
        )
        return ctx

class SearchView(Postlistview):
    def __init__(self, *args,**kwargs:Any) :
        super().__init__(*args,**kwargs)
        self._search_value=''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value=self._search_value
        return super().get_queryset().filter(
            Q(content__icontains=search_value) |
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value)
        )[:itens_por_pagina]

    def get_context_data(self,**kwargs):
        ctx=super().get_context_data(**kwargs)
        ctx.update(
            {'page_title': f"Search for '{self._search_value[:30]}' - ",
             'search_value': self._search_value,}
        )
        return ctx
    def get(self, request, *args, **kwargs):
        if self._search_value =='':
            return redirect('Blog12:index')
        return super().get(request, *args, **kwargs)



class PageDetailView(DeleteView):
    template_name = 'blog/pages/page.html'
    model = Page
    success_url = reverse_lazy('Blog12:index')
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs:Any) -> dict[str,Any]:
        ctx=super().get_context_data(**kwargs)
        page=self.get_object( )
        page_title=f"{page.title} - Pagina"
        ctx.update(
            {'page_title': page_title,}
        )
        return ctx

    def get_queryset(self)->QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DeleteView):
    template_name = 'blog/pages/post.html'
    model = Post
    success_url = reverse_lazy('Blog12:index')
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs:Any) -> dict[str,Any]:
        ctx=super().get_context_data(**kwargs)
        post=self.get_object( )
        page_title=f"{post.title} - Pagina"
        ctx.update(
            {'page_title': page_title,}
        )
        return ctx

    def get_queryset(self)->QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

