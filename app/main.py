from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI

from app.routers import health, predict


@asynccontextmanager
async def lifespan(app: FastAPI):

    caminho_modelo = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "cardiopredict_pipeline.joblib"
    )

    print("Carregando modelo CardioPredict...")

    app.state.modelo = joblib.load(caminho_modelo)

    print("Modelo carregado com sucesso!")

    yield

    app.state.modelo = None
    print("Aplicação encerrada.")


app = FastAPI(
    title="CardioPredict Clínico",
    description="API experimental para classificação de doença cardíaca utilizando Machine Learning.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health.router)
app.include_router(predict.router)