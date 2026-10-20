from ucimlrepo import fetch_ucirepo

# Carregar a base Heart Disease Cleveland
heart = fetch_ucirepo(id=45)

# Separar as variáveis
X = heart.data.features
y = heart.data.targets

# Converter o alvo em classificação binária
y_binario = (y["num"] > 0).astype(int)

# Verificar os dados
print("Base carregada com sucesso!")
print("Quantidade de registros:", len(X))
print("Quantidade de variáveis:", X.shape[1])
print("\nDistribuição das classes:")
print(y_binario.value_counts())


from sklearn.model_selection import train_test_split

# Primeira divisão: treino (60%) e temporário (40%)
X_treino, X_temporario, y_treino, y_temporario = train_test_split(
    X,
    y_binario,
    test_size=0.40,
    random_state=42,
    stratify=y_binario
)

# Segunda divisão: validação (20%) e teste (20%)
X_validacao, X_teste, y_validacao, y_teste = train_test_split(
    X_temporario,
    y_temporario,
    test_size=0.50,
    random_state=42,
    stratify=y_temporario
)

print("\nDivisão dos dados:")
print("Treinamento:", len(X_treino), "registros")
print("Validação:", len(X_validacao), "registros")
print("Teste:", len(X_teste), "registros")

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Variáveis numéricas
variaveis_numericas = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak"
]

# Variáveis categóricas
variaveis_categoricas = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal"
]

# Tratamento das variáveis numéricas
pipeline_numerico = Pipeline(steps=[
    ("imputacao", SimpleImputer(strategy="median")),
    ("escalonamento", StandardScaler())
])

# Tratamento das variáveis categóricas
pipeline_categorico = Pipeline(steps=[
    ("imputacao", SimpleImputer(strategy="most_frequent")),
    ("codificacao", OneHotEncoder(handle_unknown="ignore"))
])

# Combinar os dois pipelines
preprocessador = ColumnTransformer(transformers=[
    ("numericas", pipeline_numerico, variaveis_numericas),
    ("categoricas", pipeline_categorico, variaveis_categoricas)
])

print("\nPipeline de pré-processamento criado com sucesso!")
print("Variáveis numéricas:", len(variaveis_numericas))
print("Variáveis categóricas:", len(variaveis_categoricas))

from sklearn.ensemble import RandomForestClassifier
from sklearn.base import clone

# Construir o pipeline completo
modelo_floresta = Pipeline(steps=[
    ("preprocessamento", clone(preprocessador)),
    ("classificador", RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    ))
])

# Treinar exclusivamente com o conjunto de treinamento
modelo_floresta.fit(X_treino, y_treino)

print("\nRandom Forest treinada com sucesso!")
print("Registros utilizados:", len(X_treino))
print("Quantidade de árvores:", 200)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# Avaliar o modelo nos conjuntos de validação e teste
for nome, X_avaliacao, y_real in [
    ("VALIDAÇÃO", X_validacao, y_validacao),
    ("TESTE", X_teste, y_teste)
]:
    previsoes = modelo_floresta.predict(X_avaliacao)
    probabilidades = modelo_floresta.predict_proba(X_avaliacao)[:, 1]

    matriz = confusion_matrix(y_real, previsoes, labels=[0, 1])
    vn, fp, fn, vp = matriz.ravel()

    print(f"\n===== RESULTADOS: {nome} =====")
    print(f"Acurácia: {accuracy_score(y_real, previsoes):.4f}")
    print(f"Precisão: {precision_score(y_real, previsoes):.4f}")
    print(f"Sensibilidade: {recall_score(y_real, previsoes):.4f}")
    print(f"Especificidade: {vn / (vn + fp):.4f}")
    print(f"F1-Score: {f1_score(y_real, previsoes):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_real, probabilidades):.4f}")
    print("Matriz de confusão:")
    print(matriz)


from pathlib import Path
import joblib

# Identificar a raiz do projeto
raiz_projeto = Path(__file__).resolve().parent.parent

# Criar a pasta models
pasta_modelos = raiz_projeto / "models"
pasta_modelos.mkdir(parents=True, exist_ok=True)

# Salvar o pipeline completo em um arquivo de reprodução
caminho_modelo = pasta_modelos / "cardiopredict_pipeline.joblib"

joblib.dump(modelo_floresta, caminho_modelo)

print("\nModelo reproduzido salvo com sucesso!")
print("Arquivo:", caminho_modelo)