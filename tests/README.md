# Testes de Monitoramento — CardioPredict Clínico

## 1. Objetivo

O arquivo `test_health.py` contém testes automatizados para verificar o funcionamento do endpoint `GET /health` da API CardioPredict Clínico.

O objetivo é confirmar que a aplicação identifica corretamente a disponibilidade do modelo de Machine Learning.

Os testes são executados com `pytest` e utilizam o `TestClient` do FastAPI.

## 2. Teste 1 — API funcionando normalmente

**Função:** `test_health()`

### Objetivo

Verificar se a API retorna uma resposta de sucesso quando o modelo Random Forest está carregado corretamente.

### Funcionamento

1. O `TestClient` inicia a aplicação FastAPI.
2. O mecanismo `lifespan` carrega o modelo treinado.
3. O teste envia uma requisição `GET /health`.
4. A resposta HTTP é verificada.
5. O conteúdo JSON é comparado com o resultado esperado.

### Resultado esperado

**HTTP 200 — OK**

```json
{
  "status": "ok",
  "modelo_carregado": true
}
```

### Critérios de aprovação

- O código HTTP deve ser 200.
- O campo `status` deve apresentar o valor `"ok"`.
- O campo `modelo_carregado` deve ser `true`.

**Importância:** comprova que a aplicação foi inicializada e reconhece o modelo como disponível.

---

## 3. Teste 2 — Modelo indisponível

**Função:** `test_health_modelo_indisponivel()`

### Objetivo

Verificar se a API identifica a indisponibilidade do modelo e responde com o código HTTP adequado.

### Funcionamento

1. O `TestClient` inicia a aplicação normalmente.
2. O teste armazena uma referência ao modelo carregado.
3. A variável `app.state.modelo` é temporariamente definida como `None`.
4. Uma requisição `GET /health` é enviada.
5. O endpoint identifica que o modelo está indisponível.
6. A API retorna HTTP 503.
7. O bloco `finally` restaura a referência original ao modelo.

### Resultado esperado

**HTTP 503 — Service Unavailable**

```json
{
  "detail": "Modelo não está disponível."
}
```

### Critérios de aprovação

- O código HTTP deve ser 503.
- A mensagem deve informar que o modelo está indisponível.
- A simulação não deve modificar ou excluir o arquivo `.joblib`.

**Importância:** comprova que o sistema não informa falsamente que está operacional quando o modelo necessário à previsão está indisponível.

---

## 4. Ferramentas utilizadas

| Ferramenta | Finalidade |
|---|---|
| Python | Linguagem de programação |
| FastAPI | Desenvolvimento da API |
| pytest | Execução dos testes automatizados |
| TestClient | Simulação de requisições HTTP |
| Pydantic | Validação dos dados utilizados pela API |
| joblib | Carregamento do modelo treinado |

## 5. Como executar os testes

No terminal PowerShell, com o ambiente virtual ativado e na raiz do projeto:

```powershell
python -m pytest tests/test_health.py -v
```

O parâmetro `-v` permite visualizar individualmente os testes executados.

### Resultado esperado

```text
tests/test_health.py::test_health PASSED
tests/test_health.py::test_health_modelo_indisponivel PASSED

2 passed
```

## 6. Resultados obtidos

Na execução realizada durante o desenvolvimento, os dois testes foram aprovados.

| Teste | HTTP esperado | Resultado |
|---|---|---|
| `test_health` | 200 | PASSED |
| `test_health_modelo_indisponivel` | 503 | PASSED |

O conjunto completo da API também apresentou **7 testes aprovados**, incluindo os testes de classificação e tratamento de erros do endpoint `/predict`.

Foi observado um aviso de depreciação relacionado à integração entre Starlette e `httpx`. Esse aviso não impediu a aprovação dos testes.

## 7. Conclusão

Os testes do endpoint `/health` demonstram que a API CardioPredict Clínico consegue:

- Identificar a disponibilidade do modelo treinado.
- Responder corretamente quando o serviço está operacional.
- Reconhecer a ausência do modelo.
- Retornar HTTP 503 quando a previsão não pode ser disponibilizada.

Esses testes contribuem para a confiabilidade técnica do projeto, mas não comprovam a validade clínica das previsões.

**Observação:** o CardioPredict Clínico é um projeto experimental e educacional. Não deve ser utilizado para diagnóstico ou tomada de decisões clínicas reais.