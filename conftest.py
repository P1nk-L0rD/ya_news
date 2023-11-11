import time
from datetime import datetime, timedelta

import pytest

from news.models import News, Comment
from django.conf import settings


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=datetime.now(),
    )
    return news


@pytest.fixture
def news_pk(news):
    return news.pk,


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def many_news():
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 3):
        new_news = News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        all_news.append(new_news)
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def many_comments(author, news):
    all_comments = []
    for index in range(2):
        new_comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        all_comments.append(new_comment)
        time.sleep(0.2)
    return all_comments


@pytest.fixture
def comment_form_data(author, news):
    form = {
        "text": "Название комментария"
    }
    return form


@pytest.fixture
def home_url():
    return 'news:home'


@pytest.fixture
def detail_url():
    return 'news:detail'


@pytest.fixture
def delete_comment_url():
    return 'news:delete'


@pytest.fixture
def edit_comment_url():
    return 'news:edit'
