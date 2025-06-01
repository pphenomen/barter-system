from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm

class SignUpView(CreateView):
    """Регистрация нового пользователя"""
    form_class = UserCreationForm
    template_name = 'ads/signup.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class MyAdsView(ListView):
    """Список объявлений текущего пользователя"""
    model = Ad
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'
    ordering = ['-created_at']

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)

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
    success_url = reverse_lazy('my_ads')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return redirect('ad_list')
        return super().dispatch(request, *args, **kwargs)

class AdDeleteView(DeleteView):
    """Удаление объявления (только автор)"""
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('my_ads')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return redirect('ad_list')
        return super().dispatch(request, *args, **kwargs)
    
class ExchangeProposalCreateView(CreateView):
    """Создание предложения обмена"""
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'exchanges/exchange_form.html'
    success_url = '/'  

    def form_valid(self, form):
        form.instance.status = 'Ожидает'
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver_id = self.request.GET.get('receiver')
        if receiver_id:
            try:
                context['receiver_ad'] = Ad.objects.get(pk=receiver_id)
            except Ad.DoesNotExist:
                context['receiver_ad'] = None
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        receiver_id = self.request.GET.get('receiver')
        if receiver_id:
            initial['ad_receiver'] = receiver_id
        return initial

class ExchangeProposalListView(ListView):
    """Список предложений обмена с фильтрацией"""
    model = ExchangeProposal
    template_name = 'exchanges/exchange_list.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = ExchangeProposal.objects.all()
        status = self.request.GET.get('status')
        sender = self.request.GET.get('sender')
        receiver = self.request.GET.get('receiver')

        if status:
            queryset = queryset.filter(status=status)
        if sender:
            queryset = queryset.filter(ad_sender__user__username=sender)
        if receiver:
            queryset = queryset.filter(ad_receiver__user__username=receiver)

        return queryset

class SentProposalsView(ListView):
    """Показать предложения, отправленные текущим пользователем"""
    model = ExchangeProposal
    template_name = 'exchanges/exchange_sent.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_sender__user=self.request.user)

class ReceivedProposalsView(ListView):
    """Показать предложения, полученные текущим пользователем"""
    model = ExchangeProposal
    template_name = 'exchanges/exchange_received.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        proposal_id = request.POST.get('proposal_id')
        action = request.POST.get('action')

        if proposal_id and action in ['Принята', 'Отклонена']:
            try:
                proposal = ExchangeProposal.objects.get(pk=proposal_id, ad_receiver__user=request.user)
                proposal.status = action
                proposal.save()
            except ExchangeProposal.DoesNotExist:
                pass

        return redirect('exchange_received')