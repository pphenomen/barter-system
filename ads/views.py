from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ad
from .forms import AdForm

class AdListView(ListView):
    """Показ всех объявлений"""
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']


class AdCreateView(CreateView):
    """Создание нового объявления"""
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(UpdateView):
    """Редактирование объявления (только автор)"""
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return redirect('ad_list')
        return super().dispatch(request, *args, **kwargs)


class AdDeleteView(DeleteView):
    """Удаление объявления (только автор)"""
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return redirect('ad_list')
        return super().dispatch(request, *args, **kwargs)