

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as cliente:
        resposta = cliente.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "ok",
        "modelo_carregado": True
    }

def test_health_modelo_indisponivel():
    with TestClient(app) as cliente:
        modelo_original = app.state.modelo

        try:
            app.state.modelo = None
            resposta = cliente.get("/health")
        finally:
            app.state.modelo = modelo_original

    assert resposta.status_code == 503
    assert resposta.json()["detail"] == (
        "Modelo não está disponível."
    )
