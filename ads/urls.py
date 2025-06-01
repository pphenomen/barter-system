from django.urls import path
from .views import AdListView, AdCreateView, AdUpdateView, AdDeleteView, ExchangeProposalCreateView, ExchangeProposalListView

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('ads/new/', AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    
    path('exchange/new/', ExchangeProposalCreateView.as_view(), name='exchange_create'),
    path('exchange/', ExchangeProposalListView.as_view(), name='exchange_list'),
]
