from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from pytest_django.asserts import assertRedirects
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(
    client, comment_form_data, detail_url, news_pk
):
    url = reverse(detail_url, args=news_pk)
    client.post(url, data=comment_form_data)
    comment_amount = Comment.objects.count()
    assert comment_amount == 0


def test_user_can_create_comment(
    author_client, author, comment_form_data, detail_url, news_pk, news
):
    url = reverse(detail_url, args=news_pk)
    response = author_client.post(url, data=comment_form_data)
    assert response.url == f'/news/{news.pk}/#comments'
    comments_amount = Comment.objects.count()
    assert comments_amount == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == comment_form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_user_cant_use_bad_words(
    admin_client, news_pk, detail_url
):
    bad_words_data = {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    }
    url = reverse(detail_url, args=news_pk)
    response = admin_client.post(
        url,
        data=bad_words_data
    )
    answer_form = response.context['form']
    assert (WARNING in str(answer_form))
    comments_amount = Comment.objects.count()
    assert comments_amount == 0


def test_author_can_delete_comment(
    author_client, news, comment, delete_comment_url
):
    url = reverse(delete_comment_url, args=(comment.id,))
    response = author_client.delete(url)
    assert response.url == f'/news/{news.pk}/#comments'
    comment_amount = Comment.objects.count()
    assert comment_amount == 0


def test_user_cant_delete_comment_of_another_user(
    admin_client, comment, delete_comment_url
):
    url = reverse(delete_comment_url, args=(comment.id,))
    response = admin_client.delete(url)
    status_code = response.status_code
    assert status_code == HTTPStatus.NOT_FOUND
    comment_amount = Comment.objects.count()
    assert comment_amount == 1


def test_author_can_edit_comment(
    author_client, comment, edit_comment_url, comment_form_data,
    news
):
    url = reverse(edit_comment_url, args=(comment.id,))
    response = author_client.post(url, data=comment_form_data)
    assertRedirects(response, f'/news/{news.pk}/#comments')
    new_comment = Comment.objects.get()
    assert new_comment.text == comment_form_data['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client, comment, edit_comment_url, comment_form_data,
    news
):
    url = reverse(edit_comment_url, args=(comment.id,))
    response = admin_client.post(url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    new_comment = Comment.objects.get()
    assert new_comment.text != comment_form_data['text']
