from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (AdListView, AdCreateView, AdUpdateView, AdDeleteView, ExchangeProposalCreateView, ExchangeProposalListView, 
                    SentProposalsView, ReceivedProposalsView, MyAdsView, SignUpView)

urlpatterns = [
    # Объявления
    path('', AdListView.as_view(), name='ad_list'),
    path('ads/new/', AdCreateView.as_view(), name='ad_create'),
    path('my-ads/', MyAdsView.as_view(), name='my_ads'),
    path('ads/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),

    # Обмены
    path('exchange/', ExchangeProposalListView.as_view(), name='exchange_list'),
    path('exchange/new/', ExchangeProposalCreateView.as_view(), name='exchange_create'),
    path('exchange/sent/', SentProposalsView.as_view(), name='exchange_sent'),
    path('exchange/received/', ReceivedProposalsView.as_view(), name='exchange_received'),
    
    # Вход/регистрация
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html', next_page='ad_list'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
