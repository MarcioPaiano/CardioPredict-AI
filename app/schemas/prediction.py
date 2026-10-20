
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DadosPaciente(BaseModel):
    """Dados clínicos de entrada do modelo CardioPredict."""

    model_config = ConfigDict(extra="forbid")

    age: int = Field(
        ge=18,
        le=120,
        description="Idade do paciente em anos.",
        examples=[58]
    )

    sex: Literal[0, 1] = Field(
        description="Sexo codificado na base Cleveland: 0 = feminino; 1 = masculino.",
        examples=[1]
    )

    cp: Literal[1, 2, 3, 4] = Field(
        description=(
            "Tipo de dor torácica: "
            "1 = angina típica; "
            "2 = angina atípica; "
            "3 = dor não anginosa; "
            "4 = assintomático."
        ),
        examples=[4]
    )

    trestbps: int = Field(
        gt=0,
        le=300,
        description="Pressão arterial sistólica em repouso, em mmHg.",
        examples=[140]
    )

    chol: int = Field(
        gt=0,
        le=700,
        description="Colesterol sérico total, em mg/dL.",
        examples=[245]
    )

    fbs: Literal[0, 1] = Field(
        description=(
            "Glicemia de jejum superior a 120 mg/dL: "
            "0 = não; 1 = sim. "
            "A variável representa uma categoria, não o valor da glicemia."
        ),
        examples=[0]
    )

    restecg: Literal[0, 1, 2] = Field(
        description=(
            "Resultado do eletrocardiograma em repouso: "
            "0 = normal; "
            "1 = alterações da onda ST-T; "
            "2 = hipertrofia ventricular esquerda provável ou definida "
            "pelos critérios de Estes."
        ),
        examples=[0]
    )

    thalach: int = Field(
        gt=0,
        le=250,
        description="Frequência cardíaca máxima atingida, em batimentos por minuto.",
        examples=[150]
    )

    exang: Literal[0, 1] = Field(
        description=(
            "Angina induzida por exercício: "
            "0 = não; 1 = sim."
        ),
        examples=[1]
    )

    oldpeak: float = Field(
        ge=0,
        le=10,
        description=(
            "Depressão do segmento ST induzida por exercício "
            "em relação ao repouso."
        ),
        examples=[2.3]
    )

    slope: Literal[1, 2, 3] = Field(
        description=(
            "Inclinação do segmento ST no pico do exercício: "
            "1 = ascendente; "
            "2 = horizontal; "
            "3 = descendente."
        ),
        examples=[2]
    )

    ca: Literal[0, 1, 2, 3] = Field(
        description=(
            "Número de vasos principais (0 a 3) "
            "visualizados por fluoroscopia."
        ),
        examples=[1]
    )

    thal: Literal[3, 6, 7] = Field(
        description=(
            "Resultado codificado da variável thal na base Cleveland: "
            "3 = normal; "
            "6 = defeito fixo; "
            "7 = defeito reversível."
        ),
        examples=[7]
    )

class ResultadoPrevisao(BaseModel):
    """Resultado da classificação realizada pelo modelo."""

    classe_prevista: Literal[0, 1] = Field(
        description=(
            "Classificação estimada: 0 = ausência de doença "
            "cardíaca; 1 = presença de doença cardíaca."
        ),
        examples=[1]
    )

    probabilidade_presenca: float = Field(
        ge=0,
        le=1,
        description=(
            "Probabilidade estimada para a classe 1, "
            "em escala de 0 a 1."
        ),
        examples=[0.82]
    )
