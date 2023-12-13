from fastapi.testclient import TestClient

from fast_duno.app import app


def test_root_deve_retornar_200_e_OlaMundo():               # Definido no método AAA - Arrange, Act & Assert
    client = TestClient(app)                                # Arrange

    response = client.get('/')                              # Act

    assert response.status_code == 200                      # Assert
    assert response.json() == {'message': 'Olá, mundo!'}    # Assert
