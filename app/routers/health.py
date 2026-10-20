
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get(
    "/health",
    summary="Verificar funcionamento da API",
    description=(
        "Verifica se a API está funcionando e "
        "se o modelo de inteligência artificial está disponível."
    ),
    tags=["Monitoramento"]
)
def verificar_saude(request: Request):

    modelo = getattr(request.app.state, "modelo", None)

    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo não está disponível."
        )

    return {
        "status": "ok",
        "modelo_carregado": True
    }
