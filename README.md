# 🌟 Datathon Passos Mágicos — PosTech Fase 5

Análise de dados educacionais e modelo preditivo de risco de defasagem para a [Associação Passos Mágicos](https://passosmagicos.org.br), com dados do PEDE 2022–2024.

---

## 📁 Estrutura do Projeto

```
Postech - fase 5/
├── passos_magicos_analise.ipynb   # EDA completa + modelo preditivo (11 questões)
├── app.py                         # App Streamlit — preditor de risco
├── requirements.txt               # Dependências Python
├── README.md                      # Este arquivo
│


---

## 🚀 Como Rodar

### 1. Ambiente virtual

```bash
cd "Postech - fase 5"
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### 2. Notebook (EDA + Modelo)

Abra o Jupyter e execute célula a célula:

```bash
jupyter notebook passos_magicos_analise.ipynb
```

O notebook irá:
- Baixar a planilha diretamente do Google Drive via `gdown`
- Limpar e unificar as 3 abas (2022, 2023, 2024)
- Gerar todos os gráficos das 11 questões
- Treinar e avaliar o modelo preditivo
- Salvar `modelo_risco_defasagem.pkl` e `features_modelo.pkl`

### 3. App Streamlit

```bash
streamlit run app.py
```

Acesse em: `http://localhost:8501`

> **Nota:** Execute o notebook primeiro para gerar o `.pkl`. Sem ele, o app roda em modo demonstração com heurística simplificada.

---

## 📊 Dataset

**BASE DE DADOS PEDE 2024 — DATATHON**  
Fonte: Google Drive compartilhado pelo projeto  
ID: `1td91KoeSgXrUrCVOUkLmONG9Go3LVcXpcNEw_XrL2R0`

| Aba | Ano | Alunos | Fase |
|-----|-----|--------|------|
| Sheet 1 | 2022 | 58 | Fases 5, 6, 7 |
| Sheet 2 | 2023 | 51 | ALFA |
| Sheet 3 | 2024 | 49 | ALFA |

### Indicadores

| Sigla | Nome | Escala |
|-------|------|--------|
| IDA | Índice de Desempenho Acadêmico | 0–10 |
| IEG | Índice de Engajamento | 0–10 |
| IAA | Índice de Autoavaliação | 0–10 |
| IPS | Índice Psicossocial | 0–10 |
| IPP | Índice Psicopedagógico (2023+) | 0–10 |
| IPV | Índice do Ponto de Virada | 0–10 |
| IAN | Índice de Adequação de Nível | 0–10 |
| INDE | Índice de Desenvolvimento Educacional (composto) | 0–10 |

### Classificação (Pedra)
`Ágata` → `Quartzo` → `Topázio` → `Ametista`

---

## 🤖 Modelo Preditivo

**Objetivo:** Prever a probabilidade de um aluno entrar em risco de defasagem (DEFASAGEM < 0).

**Abordagem:**
- Algoritmos comparados: Random Forest vs Gradient Boosting
- Validação: cross-validation 5-fold estratificado + split temporal (treino: 2022–2023 / teste: 2024)
- Métricas: ROC-AUC, Precision, Recall, F1
- Explicabilidade: SHAP values

**Features principais:**
- Indicadores brutos: IDA, IEG, IPS, IPP, IAA, IPV, IAN, MAT, POR
- Features derivadas: GAP_IAA_IDA, IEG_IDA_MEDIO, IPS_IDA_RATIO

---

## 📋 Questões Respondidas

| # | Tema | Indicador |
|---|------|-----------|
| 1 | Perfil de defasagem | IAN |
| 2 | Evolução do desempenho | IDA |
| 3 | Engajamento vs desempenho | IEG × IDA × IPV |
| 4 | Coerência da autoavaliação | IAA × IDA |
| 5 | Padrões psicossociais | IPS |
| 6 | Psicopedagógico vs defasagem | IPP × IAN |
| 7 | Influências no ponto de virada | IPV |
| 8 | Combinações que elevam o INDE | IDA + IEG + IPS + IPP |
| 9 | Previsão de risco (ML) | Todos |
| 10 | Efetividade do programa | Pedra × INDE × Anos |
| 11 | Insights criativos | Análise de gênero, radar por Pedra, alertas |

---

## ☁️ Deploy (Streamlit Community Cloud)

1. Suba o repositório para o GitHub (incluindo `app.py`, `requirements.txt` e os arquivos `.pkl`)
2. Acesse [streamlit.io/cloud](https://streamlit.io/cloud) e conecte o repositório
3. Configure: **Main file path** = `app.py`
4. Clique em **Deploy**

---

## 📦 Entregáveis

- [x] `passos_magicos_analise.ipynb` — Análise e modelo preditivo
- [x] `app.py` + deploy no Streamlit Community Cloud
- [ ] Apresentação gerencial (PPT/PDF) com storytelling
- [ ] Vídeo de até 5 minutos
- [ ] Link do GitHub com o código

---

## 👥 Sobre o Projeto

**Associação Passos Mágicos** — 35 anos transformando a vida de crianças e jovens em vulnerabilidade social por meio da educação de qualidade, auxílio psicológico e ampliação de visão de mundo.

**PosTech FIAP — Datathon Fase 5**
