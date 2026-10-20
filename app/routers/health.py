from fastapi import APIRouter, Request

router = APIRouter()


@router.get(
    "/health",
    summary="Verificar funcionamento da API",
    description="Verifica se a API está funcionando e se o modelo foi carregado.",
    tags=["Monitoramento"]
)
def verificar_saude(request: Request):

    modelo = getattr(request.app.state, "modelo", None)

    if modelo is None:
        return {
            "status": "erro",
            "modelo_carregado": False
        }

    return {
        "status": "ok",
        "modelo_carregado": True
    }