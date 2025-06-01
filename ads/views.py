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
        """Устанавливает текущего пользователя как автора объявления"""
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class MyAdsView(ListView):
    """Список объявлений текущего пользователя"""
    model = Ad
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 2

    def get_queryset(self):
        """Фильтрует объявления по текущему пользователю"""
        qs = Ad.objects.filter(user=self.request.user).order_by('-created_at')
        
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        search = self.request.GET.get('q')

        if category:
            qs = qs.filter(category__icontains=category)
        if condition:
            qs = qs.filter(condition=condition)
        if search:
            qs = qs.filter(title__icontains=search)

        return qs

class AdListView(ListView):
    """Показ всех объявлений"""
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 2
    
    def get_queryset(self):
        qs = Ad.objects.all().order_by('-created_at')
        if self.request.user.is_authenticated:
            qs = qs.exclude(user=self.request.user)
        
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        search = self.request.GET.get('q')

        if category:
            qs = qs.filter(category__icontains=category)
        if condition:
            qs = qs.filter(condition=condition)
        if search:
            qs = qs.filter(title__icontains=search)    
        
        return qs

class AdCreateView(CreateView):
    """Создание нового объявления"""
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('my_ads')

    def dispatch(self, request, *args, **kwargs):
        """Ограничивает доступ только для авторизованных пользователей"""
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Устанавливает текущего пользователя как автора объявления"""
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdUpdateView(UpdateView):
    """Редактирование объявления (только автор)"""
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('my_ads')

    def dispatch(self, request, *args, **kwargs):
        """Проверяет, что текущий пользователь это автор объявления"""
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
        """Проверяет, что текущий пользователь это автор объявления"""
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
    paginate_by = 2  

    def form_valid(self, form):
        """Устанавливает статус 'Ожидает' перед сохранением предложения"""
        form.instance.status = 'Ожидает'
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        """Ограничивает доступ только для авторизованных пользователей"""
        if not request.user.is_authenticated:
            return redirect('/admin/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        """Передаёт текущего пользователя в форму для фильтрации объявлений"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Добавляет в контекст выбранное объявление-получатель"""
        context = super().get_context_data(**kwargs)
        receiver_id = self.request.GET.get('receiver')
        if receiver_id:
            try:
                context['receiver_ad'] = Ad.objects.get(pk=receiver_id)
            except Ad.DoesNotExist:
                context['receiver_ad'] = None
        return context
    
    def get_initial(self):
        """Автоматически заполняет поле отправителя"""
        initial = super().get_initial()
        receiver_id = self.request.GET.get('receiver')
        if receiver_id:
            initial['ad_receiver'] = receiver_id
        return initial

class ExchangeProposalListView(ListView):
    """Список всех предложений обмена с фильтрацией по статусу, отправителю и получателю"""
    model = ExchangeProposal
    template_name = 'exchanges/exchange_list.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']

    def get_queryset(self):
        """Применяет фильтры из GET-параметров (status, sender, receiver)"""
        queryset = ExchangeProposal.objects.all()
        status = self.request.GET.get('status')
        sender = self.request.GET.get('sender')
        receiver = self.request.GET.get('receiver')
        mine = self.request.GET.get('mine')

        if status:
            queryset = queryset.filter(status=status)
        if sender:
            queryset = queryset.filter(ad_sender__user__username=sender)
        if receiver:
            queryset = queryset.filter(ad_receiver__user__username=receiver)

        if mine == 'sent' and self.request.user.is_authenticated:
            queryset = queryset.filter(ad_sender__user=self.request.user)
        elif mine == 'received' and self.request.user.is_authenticated:
            queryset = queryset.filter(ad_receiver__user=self.request.user)
        
        return queryset

class SentProposalsView(ListView):
    """Показать предложения, отправленные текущим пользователем"""
    model = ExchangeProposal
    template_name = 'exchanges/exchange_sent.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']
    paginate_by = 2

    def get_queryset(self):
        """Фильтрует предложения, где текущий пользователь является получателем"""
        return ExchangeProposal.objects.filter(ad_sender__user=self.request.user)

class ReceivedProposalsView(ListView):
    """Показать предложения, полученные текущим пользователем"""
    model = ExchangeProposal
    template_name = 'exchanges/exchange_received.html'
    context_object_name = 'proposals'
    ordering = ['-created_at']
    paginate_by = 2

    def get_queryset(self):
        """Фильтрует предложения, где текущий пользователь является получателем"""
        return ExchangeProposal.objects.filter(ad_receiver__user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        """Обрабатывает изменение статуса предложения: принять или отклонить"""
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