import pytest
from django.shortcuts import reverse
from django.utils.timezone import now


@pytest.mark.parametrize('url', (
    'settings.base',
    'settings.registration',
    'dashboard',
    'members.typeahead',
    'members.list',
    'members.add',
    'finance.uploads.list',
    'finance.uploads.add',
    'finance.accounts.list',
    'finance.accounts.add',
    'mails.sent',
    'mails.outbox.list',
    'mails.outbox.send',
    'mails.outbox.purge',
    'mails.templates.list',
))
@pytest.mark.parametrize('logged_in', (True, False))
@pytest.mark.django_db
def test_office_access_urls(client, user, url, logged_in):
    if logged_in:
        client.force_login(user)

    response = client.get(reverse('office:{}'.format(url)), follow=True)
    assert response.status_code == 200
    assert (response.resolver_match.url_name == 'login') is not logged_in


@pytest.mark.django_db
def test_member_dashboard(full_testdata, logged_in_client, user):
    response = logged_in_client.get(reverse('office:members.dashboard', kwargs={'pk': 3}), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_member_data(full_testdata, logged_in_client, user):
    response = logged_in_client.get(reverse('office:members.data', kwargs={'pk': 3}), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_member_finance(full_testdata, logged_in_client, user):
    response = logged_in_client.get(reverse('office:members.finance', kwargs={'pk': 3}), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_member_add(full_testdata, logged_in_client, user):
    response = logged_in_client.get(reverse('office:members.add'), follow=True)
    assert response.status_code == 200

    response = logged_in_client.post(reverse('office:members.add'), {
        'member__number': '23',
        'member__name': 'Torsten Est',
        'membership__start': str(now().date()),
        'membership__interval': '1',
        'membership__amount': '10',
    }, follow=True)
    assert response.status_code == 200
    assert b'"alert alert-success"' in response.content
    assert response.resolver_match.url_name == 'members.data'


@pytest.mark.django_db
def test_transaction_detail(full_testdata, logged_in_client, user):
    # Balanced transaction
    response = logged_in_client.get(reverse('office:finance.transactions.detail', kwargs={'pk': 1}), follow=True)
    assert response.status_code == 200

    # Unbalanced transaction, credit
    response = logged_in_client.get(reverse('office:finance.transactions.detail', kwargs={'pk': 167}), follow=True)
    assert response.status_code == 200

    # Unbalanced transaction, debit
    response = logged_in_client.get(reverse('office:finance.transactions.detail', kwargs={'pk': 163}), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_account_detail(full_testdata, logged_in_client, user):
    response = logged_in_client.get(reverse('office:finance.accounts.detail', kwargs={'pk': '3'}), follow=True)
    assert response.status_code == 200
