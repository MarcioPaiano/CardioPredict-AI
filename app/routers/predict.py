
from fastapi import APIRouter, HTTPException, Request

from app.schemas.prediction import DadosPaciente, ResultadoPrevisao
from app.services.predictor import realizar_previsao


router = APIRouter()


@router.post(
    "/predict",
    response_model=ResultadoPrevisao,
    summary="Realizar classificação cardíaca",
    description="""
### Guia de preenchimento — CardioPredict Clínico

| Variável | Significado |
|---|---|
| **age** | Idade em anos |
| **sex** | Sexo: 0 = feminino; 1 = masculino |
| **cp** | Dor torácica: 1 = angina típica; 2 = atípica; 3 = não anginosa; 4 = assintomático |
| **trestbps** | Pressão arterial sistólica em repouso (mmHg). Limite operacional para processamento: 50 mmHg ou mais. |
| **chol** | Colesterol sérico (mg/dL) |
| **fbs** | Glicemia de jejum > 120 mg/dL: 0 = não; 1 = sim |
| **restecg** | ECG: 0 = normal; 1 = alteração ST-T; 2 = hipertrofia ventricular esquerda |
| **thalach** | Frequência cardíaca máxima atingida (bpm) |
| **exang** | Angina induzida por exercício: 0 = não; 1 = sim |
| **oldpeak** | Depressão do segmento ST induzida por exercício |
| **slope** | Inclinação do ST: 1 = ascendente; 2 = horizontal; 3 = descendente |
| **ca** | Número de vasos principais visualizados (0 a 3) - (Fluoroscopia)|
| **thal** | 3 = normal; 6 = defeito fixo; 7 = defeito reversível - (Perfusão miocárdica)|

**Atenção:** modelo experimental para fins educacionais.
Não utilizar para diagnóstico ou decisões clínicas reais.
""",
    tags=["Classificação cardíaca"],
    responses={
        400: {
            "description": "Dados rejeitados por regra operacional."
        },
        500: {
            "description": "Erro interno durante a previsão."
        },
        503: {
            "description": "Modelo de inteligência artificial indisponível."
        }
    }

)
def prever_doenca(dados: DadosPaciente, request: Request):
    
    if dados.trestbps < 50:
        raise HTTPException(
            status_code=400,
            detail=(
                "Pressão arterial sistólica inferior ao "
                "limite operacional de 50 mmHg."
            )
        )

    modelo = getattr(request.app.state, "modelo", None)

    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo não está disponível."
        )

    try:
        resultado = realizar_previsao(modelo, dados)
        return resultado

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao realizar a previsão."
        )
