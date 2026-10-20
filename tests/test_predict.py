
from fastapi.testclient import TestClient

from app.main import app

from unittest.mock import patch


# Paciente fictício utilizado exclusivamente para testes.
PACIENTE_TESTE = {
    "age": 58,
    "sex": 1,
    "cp": 4,
    "trestbps": 140,
    "chol": 245,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 1,
    "oldpeak": 2.3,
    "slope": 2,
    "ca": 1,
    "thal": 7
}


def test_previsao_valida():
    with TestClient(app) as cliente:
        resposta = cliente.post(
            "/predict",
            json=PACIENTE_TESTE
        )

    assert resposta.status_code == 200

    resultado = resposta.json()

    assert resultado["classe_prevista"] in [0, 1]
    assert 0 <= resultado["probabilidade_presenca"] <= 1


def test_idade_invalida():
    paciente = PACIENTE_TESTE.copy()
    paciente["age"] = 150

    with TestClient(app) as cliente:
        resposta = cliente.post(
            "/predict",
            json=paciente
        )

    assert resposta.status_code == 422


def test_modelo_indisponivel():
    with TestClient(app) as cliente:
        modelo_original = app.state.modelo

        try:
            app.state.modelo = None

            resposta = cliente.post(
                "/predict",
                json=PACIENTE_TESTE
            )
        finally:
            app.state.modelo = modelo_original

    assert resposta.status_code == 503
    assert resposta.json()["detail"] == (
        "Modelo não está disponível."
    )

def test_erro_interno_previsao():
    with TestClient(app) as cliente:
        with patch(
            "app.routers.predict.realizar_previsao",
            side_effect=RuntimeError("Falha simulada")
        ):
            resposta = cliente.post(
                "/predict",
                json=PACIENTE_TESTE
            )

    assert resposta.status_code == 500
    assert resposta.json()["detail"] == (
        "Erro interno ao realizar a previsão."
    )

def test_pressao_abaixo_limite_operacional():
    paciente = PACIENTE_TESTE.copy()
    paciente["trestbps"] = 40

    with TestClient(app) as cliente:
        resposta = cliente.post(
            "/predict",
            json=paciente
        )

    assert resposta.status_code == 400

    assert resposta.json()["detail"] == (
        "Pressão arterial sistólica inferior ao "
        "limite operacional de 50 mmHg."
    )


