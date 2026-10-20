# Documentação dos Testes de Previsão — CardioPredict Clínico

## 1. Objetivo

O arquivo `tests/test_predict.py` contém testes automatizados para verificar o funcionamento do endpoint `POST /predict` da API CardioPredict Clínico.

Esse endpoint recebe 13 características clínicas, realiza a validação dos dados com Pydantic e utiliza um modelo Random Forest previamente treinado para estimar a presença ou ausência de doença cardíaca, conforme a classificação da base Cleveland.

Os testes verificam tanto o funcionamento normal da previsão quanto o tratamento de entradas inválidas e falhas operacionais.

**Importante:** o CardioPredict é um projeto experimental e educacional. Suas previsões não representam diagnóstico clínico nem estimativa validada de risco futuro de infarto.

---

## 2. Ferramentas utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação |
| pytest | Execução dos testes automatizados |
| FastAPI | Framework da API |
| TestClient | Simulação de requisições HTTP |
| Pydantic | Validação dos dados clínicos |
| unittest.mock.patch | Simulação controlada de falhas |
| scikit-learn | Execução do pipeline de Machine Learning |
| joblib | Carregamento do modelo treinado |

## 3. Dados utilizados nos testes

Os testes utilizam um conjunto de dados fictícios, definido no dicionário `PACIENTE_TESTE`.

```json
{
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
```

### Significado das variáveis

| Variável | Descrição |
|---|---|
| `age` | Idade em anos |
| `sex` | Sexo codificado: 0 = feminino; 1 = masculino |
| `cp` | Categoria de dor torácica |
| `trestbps` | Pressão arterial sistólica em repouso, em mmHg |
| `chol` | Colesterol sérico, em mg/dL |
| `fbs` | Indicador de glicemia de jejum superior a 120 mg/dL |
| `restecg` | Categoria do eletrocardiograma em repouso |
| `thalach` | Frequência cardíaca máxima atingida |
| `exang` | Presença de angina induzida por exercício |
| `oldpeak` | Depressão do segmento ST induzida por exercício |
| `slope` | Categoria de inclinação do segmento ST |
| `ca` | Número de vasos principais visualizados por fluoroscopia, conforme codificação Cleveland |
| `thal` | Categoria do resultado do exame relacionado à perfusão miocárdica |

Esses valores são utilizados exclusivamente para testes de software.

---

## 4. Teste 1 — Previsão com dados válidos

**Função:** `test_previsao_valida()`

### Objetivo

Confirmar que o endpoint `/predict` recebe dados válidos, executa o modelo de Machine Learning e retorna uma resposta HTTP 200.

### Funcionamento

1. O `TestClient` inicializa a aplicação FastAPI.
2. O mecanismo `lifespan` carrega o pipeline treinado.
3. O teste envia o dicionário `PACIENTE_TESTE` para `/predict`.
4. A API valida os 13 campos.
5. O serviço de previsão executa a Random Forest.
6. O teste verifica o código HTTP e os valores retornados.

### Resultado esperado

**HTTP 200 — OK**

Exemplo ilustrativo de resposta:

```json
{
  "classe_prevista": 1,
  "probabilidade_presenca": 0.82
}
```

Os valores reais são calculados pelo modelo e podem ser diferentes dos apresentados no exemplo.

### Critérios de aprovação

- O código HTTP deve ser 200.
- `classe_prevista` deve ser 0 ou 1.
- `probabilidade_presenca` deve estar entre 0 e 1.

**Importância:** demonstra a integração entre a API, a validação Pydantic, o pipeline de pré-processamento e o classificador Random Forest.

---

## 5. Teste 2 — Idade inválida

**Função:** `test_idade_invalida()`

### Objetivo

Verificar se a API rejeita um valor de idade que ultrapassa o limite definido no esquema Pydantic.

### Funcionamento

1. O teste cria uma cópia de `PACIENTE_TESTE`.
2. O campo `age` é alterado para 150.
3. A requisição é enviada para `/predict`.
4. O Pydantic identifica que o valor ultrapassa o limite máximo de 120 anos.
5. A requisição é rejeitada antes da execução do modelo.

### Resultado esperado

**HTTP 422 — Unprocessable Content**

A resposta contém informações sobre o campo inválido e a regra de validação violada.

### Critério de aprovação

```python
assert resposta.status_code == 422
```

**Importância:** comprova que o sistema realiza a validação automática das entradas, reduzindo o risco de processar dados fora das restrições definidas.

---

## 6. Teste 3 — Modelo indisponível

**Função:** `test_modelo_indisponivel()`

### Objetivo

Confirmar que o endpoint identifica a indisponibilidade do modelo de Machine Learning.

### Funcionamento

1. O `TestClient` inicializa a aplicação.
2. O teste guarda uma referência ao modelo original.
3. A variável `app.state.modelo` é temporariamente definida como `None`.
4. Uma requisição válida é enviada para `/predict`.
5. O endpoint identifica que não existe modelo disponível para previsão.
6. A API retorna HTTP 503.
7. O bloco `finally` restaura a referência original.

### Resultado esperado

**HTTP 503 — Service Unavailable**

```json
{
  "detail": "Modelo não está disponível."
}
```

### Critérios de aprovação

- O código HTTP deve ser 503.
- A mensagem deve indicar a indisponibilidade do modelo.
- O teste não deve modificar ou excluir o arquivo `.joblib`.

**Importância:** verifica o tratamento de uma falha operacional que impede a execução das previsões.

---

## 7. Teste 4 — Erro interno durante a previsão

**Função:** `test_erro_interno_previsao()`

### Objetivo

Verificar se a API trata uma falha inesperada durante a execução da função de previsão.

### Funcionamento

1. O teste inicializa a aplicação com `TestClient`.
2. A ferramenta `unittest.mock.patch` substitui temporariamente a função `realizar_previsao`.
3. A função simulada provoca um `RuntimeError`.
4. O endpoint captura a exceção.
5. A API retorna uma resposta HTTP 500 com uma mensagem controlada.
6. Ao finalizar o contexto `patch`, a função original é restaurada.

### Resultado esperado

**HTTP 500 — Internal Server Error**

```json
{
  "detail": "Erro interno ao realizar a previsão."
}
```

### Critérios de aprovação

- O código HTTP deve ser 500.
- A mensagem retornada deve corresponder à mensagem definida na API.
- A resposta não deve expor detalhes internos da exceção simulada.

**Importância:** comprova que o sistema consegue responder de maneira controlada a falhas inesperadas no processamento.

---

## 8. Teste 5 — Pressão arterial abaixo do limite operacional

**Função:** `test_pressao_abaixo_limite_operacional()`

### Objetivo

Verificar se o endpoint rejeita uma requisição que viola uma regra operacional adicional do projeto.

### Regra implementada

Para o processamento experimental, foi definido um limite operacional mínimo de 50 mmHg para a pressão arterial sistólica em repouso (`trestbps`).

Valores positivos inferiores a esse limite são rejeitados pelo endpoint.

Esse limite constitui uma decisão de implementação do projeto, não um critério clínico validado nem uma afirmação de impossibilidade fisiológica.

### Funcionamento

1. O teste cria uma cópia de `PACIENTE_TESTE`.
2. O campo `trestbps` é alterado para 40.
3. O Pydantic aceita o valor por ser um número positivo dentro do limite estrutural definido.
4. O endpoint aplica a regra operacional adicional.
5. A requisição é rejeitada com HTTP 400.

### Resultado esperado

**HTTP 400 — Bad Request**

```json
{
  "detail": "Pressão arterial sistólica inferior ao limite operacional de 50 mmHg."
}
```

### Critérios de aprovação

- O código HTTP deve ser 400.
- A mensagem deve informar o motivo da rejeição.
- O modelo não deve ser executado para essa requisição.

**Importância:** demonstra a diferença entre validação estrutural realizada pelo Pydantic e uma regra operacional implementada no endpoint.

---

## 9. Como executar os testes

Abra o terminal PowerShell na raiz do projeto, com o ambiente virtual ativado.

### Executar apenas os testes de previsão

```powershell
python -m pytest tests/test_predict.py -v
```

### Executar todos os testes da API

```powershell
python -m pytest tests/ -v
```

O parâmetro `-v` apresenta os nomes e os resultados individuais dos testes.

## 10. Resultados obtidos

Na execução realizada durante o desenvolvimento, todos os cinco testes de previsão foram aprovados.

| Teste | HTTP esperado | Resultado |
|---|---|---|
| `test_previsao_valida` | 200 | PASSED |
| `test_idade_invalida` | 422 | PASSED |
| `test_modelo_indisponivel` | 503 | PASSED |
| `test_erro_interno_previsao` | 500 | PASSED |
| `test_pressao_abaixo_limite_operacional` | 400 | PASSED |

### Resultado do conjunto completo

**7 testes aprovados**, incluindo:

- 2 testes do endpoint `/health`.
- 5 testes do endpoint `/predict`.

A última execução informada apresentou:

```text
7 passed, 1 warning in 4.55s
```

O aviso observado foi `StarletteDeprecationWarning`, relacionado à integração entre Starlette e `httpx`. Ele não causou falha nos testes.

## 11. Limitações

A aprovação desses testes demonstra o comportamento esperado nos cenários implementados, mas não garante a ausência de todos os possíveis defeitos.

Os testes não substituem:

- Avaliação de desempenho sob carga.
- Testes completos de segurança.
- Validação com dados externos independentes.
- Avaliação de calibração das probabilidades.
- Validação clínica prospectiva.

O modelo foi desenvolvido com o conjunto Cleveland, que possui características e limitações próprias.

## 12. Conclusão

Os testes automatizados do endpoint `/predict` demonstraram que o CardioPredict Clínico consegue:

1. Processar uma requisição válida e retornar uma classificação.
2. Rejeitar entradas incompatíveis com o esquema Pydantic.
3. Identificar a indisponibilidade do modelo.
4. Tratar falhas inesperadas durante a previsão.
5. Aplicar uma regra operacional adicional de validação.

Os resultados contribuem para a qualidade, a rastreabilidade e a manutenção do software desenvolvido como projeto educacional do SENAI.

**Aviso:** o CardioPredict Clínico não é um dispositivo médico validado e não deve ser utilizado para diagnóstico, definição de tratamento ou decisões clínicas reais.