import pytest

from django.urls import reverse
from django.conf import settings


@pytest.mark.django_db
def test_news_count(many_news, admin_client, home_url):
    url = reverse(home_url)
    response = admin_client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(many_news, admin_client, home_url):
    url = reverse(home_url)
    response = admin_client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(many_comments, news):
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('admin_client'), True),
    )
)
def test_client_form(news_pk, detail_url, parametrized_client, status):
    url = reverse(detail_url, args=news_pk)
    response = parametrized_client.get(url)
    assert ('form' in response.context) == status
