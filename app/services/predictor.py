import pandas as pd


def realizar_previsao(modelo, dados_paciente):

    dados = dados_paciente.model_dump()

    tabela = pd.DataFrame([dados])

    classe = int(modelo.predict(tabela)[0])

    probabilidade = float(
        modelo.predict_proba(tabela)[0][1]
    )

    return {
        "classe_prevista": classe,
        "probabilidade_presenca": round(probabilidade, 4)
    }