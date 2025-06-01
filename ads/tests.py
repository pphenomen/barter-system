from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Телефон',
            description='Почти новый',
            category='Электроника',
            condition='Новый'
        )

    def test_ad_created(self):
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(self.ad.title, 'Телефон')

    def test_ad_edit(self):
        self.ad.title = 'Смартфон'
        self.ad.save()
        self.assertEqual(Ad.objects.first().title, 'Смартфон')

    def test_ad_delete(self):
        self.ad.delete()
        self.assertEqual(Ad.objects.count(), 0)

class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.sender_user = User.objects.create_user(username='sender', password='123')
        self.receiver_user = User.objects.create_user(username='receiver', password='456')

        self.ad_sender = Ad.objects.create(
            user=self.sender_user,
            title='Книга',
            description='Хорошее состояние',
            category='Личные вещи',
            condition='Б/у'
        )
        self.ad_receiver = Ad.objects.create(
            user=self.receiver_user,
            title='Часы',
            description='Почти новые',
            category='Личные вещи',
            condition='Новый'
        )
        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad_sender,
            ad_receiver=self.ad_receiver,
            comment='Обмен интересен?',
            status='Ожидает'
        )

    def test_proposal_created(self):
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(self.proposal.status, 'Ожидает')

    def test_proposal_status_update(self):
        self.proposal.status = 'Принята'
        self.proposal.save()
        self.assertEqual(ExchangeProposal.objects.first().status, 'Принята')

    def test_filter_by_status(self):
        results = ExchangeProposal.objects.filter(status='Ожидает')
        self.assertIn(self.proposal, results)

    def test_filter_by_sender_user(self):
        results = ExchangeProposal.objects.filter(ad_sender__user__username='sender')
        self.assertIn(self.proposal, results)

    def test_filter_by_receiver_user(self):
        results = ExchangeProposal.objects.filter(ad_receiver__user__username='receiver')
        self.assertIn(self.proposal, results)
