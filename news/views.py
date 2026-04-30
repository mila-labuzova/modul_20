from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'news/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post_detail'


class PostSearch(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.post_filtered = PostFilter(self.request.GET, queryset)
        return self.post_filtered.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_filtered'] = self.post_filtered
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'articles' in self.request.path:
            post.type = 'AR'
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    context_object_name = 'post'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')
