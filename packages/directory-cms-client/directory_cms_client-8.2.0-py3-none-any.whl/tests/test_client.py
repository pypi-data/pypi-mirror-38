import pytest
import requests_mock

from django.core.cache import caches

from directory_cms_client import DirectoryCMSClient
from directory_cms_client.version import __version__


@pytest.fixture
def default_client():
    return DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        default_service_name='foo'
    )


@pytest.fixture
def cms_cache():
    return caches['cms_fallback']


@pytest.fixture(autouse=True)
def clear_cms_cache(cms_cache):
    cms_cache.clear()


def test_cms_client_list_by_page_type_draft(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/')
        default_client.list_by_page_type('thing', draft_token='draft-token')
        request = mock.request_history[0]

        assert request.qs == {
            'draft_token': ['draft-token'],
            'fields': ['*'],
            'type': ['thing'],
        }


def test_cms_client_lookup_by_slug_language(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-slug/thing/')
        default_client.lookup_by_slug('thing', language_code='de')
        request = mock.request_history[0]

        assert request.qs == {
            'service_name': ['foo'],
            'lang': ['de'],
            'fields': ['*'],
        }


def test_cms_client_lookup_by_slug_draft(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-slug/thing/')
        default_client.lookup_by_slug('thing', draft_token='draft-token')
        request = mock.request_history[0]

        assert request.qs == {
            'service_name': ['foo'],
            'draft_token': ['draft-token'],
            'fields': ['*'],
        }


def test_cms_client_lookup_by_slug(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-slug/thing/')
        default_client.lookup_by_slug('thing')
        request = mock.request_history[0]

        assert request.qs == {
            'service_name': ['foo'],
            'fields': ['*'],
        }


def test_cms_client_lookup_by_full_path_language(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-full-path/')
        default_client.lookup_by_full_path('thing', language_code='de')
        request = mock.request_history[0]

        assert request.qs == {
            'lang': ['de'],
            'fields': ['*'],
            'full_path': ['thing'],
            'service_name': ['foo'],
        }


def test_cms_client_lookup_by_full_path_draft(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-full-path/')
        default_client.lookup_by_full_path('thing', draft_token='draft-token')
        request = mock.request_history[0]

        assert request.qs == {
            'draft_token': ['draft-token'],
            'fields': ['*'],
            'full_path': ['thing'],
            'service_name': ['foo'],
        }


def test_cms_client_lookup_by_full_path(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-full-path/')
        default_client.lookup_by_full_path('thing')
        request = mock.request_history[0]

        assert request.qs == {
            'fields': ['*'],
            'full_path': ['thing'],
            'service_name': ['foo'],
        }


def test_cms_client_lookup_by_full_path_service_name(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-full-path/')
        default_client.lookup_by_full_path(
            'thing', service_name='test-service')
        request = mock.request_history[0]

        assert request.qs == {
            'fields': ['*'],
            'full_path': ['thing'],
            'service_name': ['test-service'],
        }


def test_cms_client_lookup_by_tag_draft(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-tag/thing/')
        default_client.lookup_by_tag('thing', draft_token='draft-token')
        request = mock.request_history[0]

        assert request.qs == {
            'fields': ['*'],
            'draft_token': ['draft-token'],
            'service_name': ['foo'],
        }


def test_cms_client_lookup_by_tag(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-tag/thing/')
        default_client.lookup_by_tag('thing')
        request = mock.request_history[0]

        assert request.qs == {
            'fields': ['*'],
            'service_name': ['foo'],
        }


def test_cms_client_lookup_by_tag_service_name(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/api/pages/lookup-by-tag/thing/')
        default_client.lookup_by_tag(
            'thing', service_name='test-service')
        request = mock.request_history[0]

        assert request.qs == {
            'fields': ['*'],
            'service_name': ['test-service'],
        }


def test_timeout(default_client):
    assert default_client.timeout == 5


def test_sender_id(default_client):
    assert default_client.request_signer.sender_id == 'test-sender'


def test_version():
    assert DirectoryCMSClient.version == __version__


def test_ping(default_client):
    with requests_mock.mock() as mock:
        mock.get('http://example.com/healthcheck/ping/')
        default_client.ping()
