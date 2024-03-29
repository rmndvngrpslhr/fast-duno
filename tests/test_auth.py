from fastapi.testclient import TestClient
from freezegun import freeze_time

from fast_duno.app import app

client = TestClient(app)


def test_token_expired_after_time(client, user):
    with freeze_time('2024-01-25 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2024-01-25 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect e-mail.'}


def test_token_wrong_password(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect password.'}


def test_refresh_token(client, user, token):
    response = client.post(
        'auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2024-01-25 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2024-01-25 12:31:00'):
        response = client.post(
            'auth/refresh_token',
            headers={'Authorization': f'Bearer: {token}'},
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'Not authenticated'}
