# ============================================================
# SISTEMA INTELIGENTE DE PREDIÇÃO TÉRMICA EM ESTUFAS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

# ============================================================
# CONFIGURAÇÕES
# ============================================================

st.set_page_config(
    layout="wide",
    page_title="Sistema Inteligente de Estufas"
)

sns.set_theme()

# ============================================================
# TÍTULO
# ============================================================

st.title("🌱 Sistema Inteligente de Predição Térmica em Estufas Agrícolas")

st.markdown("""
## Modelagem Dinâmica da Transferência de Calor aplicada à Engenharia de Biossistemas

Sistema baseado em:

- Sensores IoT
- Sistemas Dinâmicos
- Equações Diferenciais
- Método de Euler
- Grid Search
- Inteligência Artificial
""")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Configurações")

cenario = st.sidebar.selectbox(
    "Escolha o cenário térmico",
    [
        "Cenário 1 - Ambiente Frio",
        "Cenário 2 - Ambiente Ideal",
        "Cenário 3 - Ambiente Quente",
        "Cenário 4 - Ambiente Crítico"
    ]
)

# ============================================================
# BASES DE DADOS
# ============================================================

if cenario == "Cenário 1 - Ambiente Frio":

    tempo = np.array([0,10,20,30,40,50])

    T_real = np.array([15,16,17,17,18,18])

    T_ext = 10

elif cenario == "Cenário 2 - Ambiente Ideal":

    tempo = np.array([0,10,20,30,40,50])

    T_real = np.array([22,23,23,24,24,25])

    T_ext = 20

elif cenario == "Cenário 3 - Ambiente Quente":

    tempo = np.array([0,10,20,30,40,50])

    T_real = np.array([27,28,29,30,31,32])

    T_ext = 35

else:

    tempo = np.array([0,10,20,30,40,50])

    T_real = np.array([33,34,35,36,37,39])

    T_ext = 42

# ============================================================
# DATAFRAME
# ============================================================

base = pd.DataFrame({

    "Tempo": tempo,

    "Temperatura Interna": T_real,

    "Temperatura Externa": T_ext

})

# ============================================================
# 1. CAPTAÇÃO DOS DADOS
# ============================================================

st.header("1. Captação dos Dados Ambientais")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Código Python")

    st.code('''
tempo = np.array([0,10,20,30,40,50])

T_real = np.array([22,23,23,24,24,25])

T_ext = 20
''', language='python')

with col2:

    st.subheader("Base de Dados")

    st.dataframe(
        base,
        use_container_width=True
    )

# ============================================================
# 2. MODELO MATEMÁTICO
# ============================================================

st.header("2. Modelo Matemático da Transferência de Calor")

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Equação Diferencial")

    st.latex(
        r"\frac{dT}{dt}=k(T_{ext}-T)"
    )

    st.markdown("""
### Onde:

- T = temperatura interna
- T_ext = temperatura externa
- k = coeficiente térmico
""")

with col2:

    st.info("""
O modelo descreve a dinâmica térmica da estufa.

A temperatura interna tende a se aproximar
da temperatura externa ao longo do tempo.
""")

# ============================================================
# 3. MÉTODO DE EULER
# ============================================================

st.header("3. Método Numérico de Euler")

col1, col2 = st.columns([1,2])

with col1:

    st.latex(
        r"T_{novo}=T+k(T_{ext}-T)"
    )

    st.code('''
T_novo = T + k*(T_ext - T)
''', language='python')

with col2:

    st.markdown("""
O Método de Euler aproxima numericamente
a solução da equação diferencial.

O sistema calcula:

- temperatura futura;
- evolução térmica;
- comportamento dinâmico.
""")

# ============================================================
# 4. SISTEMA DINÂMICO
# ============================================================

st.header("4. Sistema Dinâmico Inteligente")

st.markdown("""
O sistema aprende automaticamente o melhor coeficiente térmico k.

O coeficiente k representa:

- velocidade de troca térmica;
- isolamento da estufa;
- eficiência térmica;
- comportamento térmico do biossistema.
""")

# ============================================================
# 5. GRID SEARCH
# ============================================================

st.header("5. Otimização com Grid Search")

col1, col2 = st.columns([1,2])

with col1:

    st.code('''
valores_k = np.arange(0.001,0.10,0.001)

for k in valores_k:

    # calcula previsões

    # calcula RMSE

    # escolhe melhor k
''', language='python')

with col2:

    melhor_rmse = 999999

    melhor_k = 0

    melhor_prev = []

    valores_k = np.arange(0.001,0.10,0.001)

    for k in valores_k:

        previsoes = []

        T_modelo = T_real[0]

        previsoes.append(T_modelo)

        for i in range(1, len(T_real)):

            T_novo = T_modelo + k * (T_ext - T_modelo)

            previsoes.append(T_novo)

            T_modelo = T_novo

        previsoes = np.array(previsoes)

        rmse = np.sqrt(
            np.mean(
                (T_real - previsoes)**2
            )
        )

        if rmse < melhor_rmse:

            melhor_rmse = rmse

            melhor_k = k

            melhor_prev = previsoes

    st.success("✅ Otimização concluída")

    st.metric(
        "Melhor k",
        round(melhor_k,5)
    )

    st.metric(
        "RMSE",
        round(melhor_rmse,5)
    )

# ============================================================
# FUNÇÃO OBJETIVO
# ============================================================

st.subheader("Função Objetivo")

st.latex(
    r"RMSE=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2}"
)

# ============================================================
# 6. COMPARAÇÃO
# ============================================================

st.header("6. Comparação entre Temperatura Real e Prevista")

col1, col2 = st.columns([1,2])

with col1:

    st.code('''
plt.plot(T_real)

plt.plot(melhor_prev)
''', language='python')

with col2:

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        tempo,
        T_real,
        'o-',
        linewidth=3,
        label='Temperatura Real'
    )

    ax.plot(
        tempo,
        melhor_prev,
        's--',
        linewidth=3,
        label='Temperatura Prevista'
    )

    ax.set_xlabel("Tempo")

    ax.set_ylabel("Temperatura")

    ax.set_title(
        "Sistema Dinâmico de Transferência de Calor"
    )

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)

# ============================================================
# 7. ERRO
# ============================================================

st.header("7. Análise do Erro do Modelo")

col1, col2 = st.columns([1,2])

with col1:

    st.markdown("""
### RMSE

O RMSE mede:

- distância entre:
    - valor real;
    - valor previsto.

Quanto menor o RMSE:

✅ melhor o modelo.
""")

with col2:

    erro = T_real - melhor_prev

    erro_df = pd.DataFrame({

        "Tempo": tempo,

        "Erro": np.round(erro,3)

    })

    st.dataframe(
        erro_df,
        use_container_width=True
    )

# ============================================================
# 8. SISTEMA INTELIGENTE
# ============================================================

st.header("8. Sistema Inteligente de Tomada de Decisão")

col1, col2 = st.columns([1,2])

with col1:

    st.code('''
if temperatura < 18:

    ligar aquecimento

elif temperatura < 26:

    ambiente ideal

elif temperatura < 32:

    ligar ventilação

else:

    acionar exaustores
''', language='python')

with col2:

    analise = []

    for valor in melhor_prev:

        if valor < 18:

            estado = "FRIO"

            decisao = "🔥 Ligar aquecimento"

        elif valor < 26:

            estado = "IDEAL"

            decisao = "✅ Ambiente estável"

        elif valor < 32:

            estado = "QUENTE"

            decisao = "🌬️ Ligar ventilação"

        else:

            estado = "CRÍTICO"

            decisao = "🚨 Acionar exaustores"

        analise.append([

            round(valor,2),

            estado,

            decisao
        ])

    analise_df = pd.DataFrame(

        analise,

        columns=[
            "Temperatura Prevista",
            "Estado",
            "Decisão"
        ]
    )

    st.dataframe(
        analise_df,
        use_container_width=True
    )

# ============================================================
# 9. ZONAS TÉRMICAS
# ============================================================

st.header("9. Visualização das Zonas Térmicas")

fig2, ax2 = plt.subplots(figsize=(11,5))

ax2.plot(
    tempo,
    melhor_prev,
    'o-',
    linewidth=3,
    label='Temperatura Prevista'
)

ax2.axhspan(
    0,
    18,
    color='blue',
    alpha=0.15,
    label='Frio'
)

ax2.axhspan(
    18,
    26,
    color='green',
    alpha=0.15,
    label='Ideal'
)

ax2.axhspan(
    26,
    32,
    color='orange',
    alpha=0.15,
    label='Quente'
)

ax2.axhspan(
    32,
    45,
    color='red',
    alpha=0.15,
    label='Crítico'
)

ax2.set_xlabel("Tempo")

ax2.set_ylabel("Temperatura")

ax2.set_title(
    "Zonas Inteligentes da Estufa"
)

ax2.grid(True)

handles, labels = ax2.get_legend_handles_labels()

by_label = dict(zip(labels, handles))

ax2.legend(
    by_label.values(),
    by_label.keys()
)

st.pyplot(fig2)

# ============================================================
# 10. SIDEBAR INTELIGENTE
# ============================================================

st.sidebar.header("🌱 Estado do Biossistema")

temperatura_atual = melhor_prev[-1]

if temperatura_atual < 18:

    estado = "FRIO"

    decisao = "🔥 Ligar aquecimento"

elif temperatura_atual < 26:

    estado = "IDEAL"

    decisao = "✅ Ambiente estável"

elif temperatura_atual < 32:

    estado = "QUENTE"

    decisao = "🌬️ Ligar ventilação"

else:

    estado = "CRÍTICO"

    decisao = "🚨 Acionar exaustores"

st.sidebar.metric(
    "Temperatura Prevista",
    f"{temperatura_atual:.2f} °C"
)

st.sidebar.metric(
    "Melhor k",
    round(melhor_k,5)
)

st.sidebar.metric(
    "RMSE",
    round(melhor_rmse,5)
)

st.sidebar.subheader("Estado Atual")

st.sidebar.info(estado)

st.sidebar.subheader("Decisão Inteligente")

st.sidebar.success(decisao)

# ============================================================
# VELOCÍMETRO
# ============================================================

fig_gauge = go.Figure(go.Indicator(

    mode="gauge+number",

    value=float(temperatura_atual),

    title={'text': "Temperatura Prevista"},

    gauge={

        'axis': {'range': [0,45]},

        'steps': [

            {'range': [0,18], 'color': "blue"},

            {'range': [18,26], 'color': "green"},

            {'range': [26,32], 'color': "orange"},

            {'range': [32,45], 'color': "red"}

        ]
    }
))

st.sidebar.plotly_chart(
    fig_gauge,
    use_container_width=True
)