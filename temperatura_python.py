# ============================================================
# SISTEMA DINÂMICO DE TEMPERATURA
# Modelagem Matemática + Otimização
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURAÇÕES
# ============================================================

st.set_page_config(layout="wide")

sns.set_theme()

# ============================================================
# TÍTULO
# ============================================================

st.title("Sistema Inteligente para Modelagem Dinâmica da Temperatura 🌡️")
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "Logo_Unesp.png",
        width=650
    )
st.markdown(
    "<h3 style='text-align: center;'>Desenvolvido por Prof. Dr. Ronnie Shida Marinho</h3>",
    unsafe_allow_html=True
)
# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.image("Logo_Unesp.png", use_container_width=True)

st.sidebar.header("⚙️ Configurações")

cenario = st.sidebar.selectbox(
    "Escolha o cenário térmico",
    [
        "Ambiente Controlado",
        "Ambiente Moderado",
        "Ambiente Crítico"
    ]
)

# ============================================================
# BASES DE DADOS
# ============================================================

if cenario == "Ambiente Controlado":

    tempo = np.array([0,10,20,30,40])

    temperatura = np.array([20.0,20.2,20.7,21.4,22.3])

elif cenario == "Ambiente Moderado":

    tempo = np.array([0,10,20,30,40])

    temperatura = np.array([24,25,26.5,28,30])

else:

    tempo = np.array([0,10,20,30,40])

    temperatura = np.array([28,30,33,37,42])

# dataframe

base = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": temperatura
})

# ============================================================
# 1. CAPTAÇÃO DE DADOS
# ============================================================

st.header("1. Captação dos Dados")

col1, col2 = st.columns([1,2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
import pandas as pd

base = pd.read_csv("dados_temperatura.csv")

tempo = base["Tempo"].values

temperatura = base["Temperatura"].values
''', language='python')

# ------------------------------------------------------------
# DIREITA -> DADOS
# ------------------------------------------------------------

with col2:

    st.subheader("Dados Capturados")

    st.dataframe(
        base,
        use_container_width=True
    )

# ============================================================
# ============================================================
# 2. TAXA DE VARIAÇÃO
# ============================================================

st.header("2. Taxa de Variação da Temperatura")

col1, col2 = st.columns([1,2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO PYTHON
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
# cálculo da taxa de variação

taxas = []

for i in range(len(temperatura)-1):

    # derivada aproximada

    taxa = (
        temperatura[i+1] - temperatura[i]
    ) / (
        tempo[i+1] - tempo[i]
    )

    taxas.append(taxa)

taxas = np.array(taxas)
''', language='python')

# ------------------------------------------------------------
# DIREITA -> FÓRMULAS + RESULTADOS
# ------------------------------------------------------------

with col2:

    st.subheader("Equações Matemáticas")

    st.markdown("""
A taxa de variação mede:

- como a temperatura muda no tempo;
- velocidade de crescimento;
- dinâmica do sistema.
""")

    # derivada

    st.latex(
        r"\frac{dT}{dt}"
    )

    st.markdown("""
### Aproximação Numérica
""")

    st.latex(
        r"\frac{dT}{dt}\approx\frac{T_{i+1}-T_i}{t_{i+1}-t_i}"
    )

    st.markdown("""
### Interpretação

- numerador:
    - variação da temperatura;

- denominador:
    - variação do tempo;

- resultado:
    - velocidade de crescimento da temperatura.
""")

    # --------------------------------------------------------
    # CÁLCULO DAS TAXAS
    # --------------------------------------------------------

    taxas = []

    for i in range(len(temperatura)-1):

        taxa = (
            temperatura[i+1] - temperatura[i]
        ) / (
            tempo[i+1] - tempo[i]
        )

        taxas.append(taxa)

    taxas = np.array(taxas)

    # dataframe

    taxa_df = pd.DataFrame({
        "Intervalo": [
            "0-10",
            "10-20",
            "20-30",
            "30-40"
        ],
        "dT/dt": np.round(taxas,4)
    })

    st.subheader("Tabela das Taxas")

    st.dataframe(
        taxa_df,
        use_container_width=True
    )

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(9,4))

    ax.plot(
        tempo[1:],
        taxas,
        'o-',
        linewidth=3,
        label='dT/dt'
    )

    ax.set_xlabel("Tempo")

    ax.set_ylabel("dT/dt")

    ax.set_title(
        "Taxa de Crescimento da Temperatura"
    )

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)

# 3. SISTEMA DINÂMICO
# ============================================================

st.header("3. Sistema Dinâmico")

col1, col2 = st.columns([1, 2])

# ------------------------------------------------------------
# ESQUERDA -> EQUAÇÃO
# ------------------------------------------------------------

with col1:
    st.subheader("Modelo Matemático")

    st.latex(
        r"\frac{dT}{dt}=kT"
    )

    st.markdown("""
Hipótese:

- a taxa de crescimento
da temperatura é proporcional
à própria temperatura.
""")

    st.latex(
        r"T(t)=T_0e^{kt}"
    )

# ------------------------------------------------------------
# DIREITA -> EXPLICAÇÃO
# ------------------------------------------------------------

with col2:
    st.info(
        "O sistema aprende o comportamento "
        "dinâmico da temperatura."
    )

    st.markdown("""
### Interpretação

- se k > 0:
    - crescimento térmico;

- se k < 0:
    - resfriamento;

- quanto maior k:
    - maior velocidade de crescimento.
""")

    # ============================================================
    # 3. ESTIMAÇÃO DO PARÂMETRO k
    # ============================================================

st.header("4. Estimação do Parâmetro k")

col1, col2 = st.columns([1, 2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO PYTHON
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
# estimação de k

k_valores = []

for i in range(len(taxas)):

    k = taxas[i] / temperatura[i]

    k_valores.append(k)

k_valores = np.array(k_valores)

# média de k

k_medio = np.mean(k_valores)
''', language='python')

# ------------------------------------------------------------
# DIREITA -> FÓRMULAS + RESULTADOS
# ------------------------------------------------------------

with col2:

    st.subheader("Modelo Matemático")

    st.markdown("""
Sabemos que:
""")

    st.latex(
        r"\frac{dT}{dt}=kT"
    )

    st.markdown("""
Isolando k:
""")

    st.latex(
        r"k=\frac{\frac{dT}{dt}}{T}"
    )

    st.markdown("""
### Interpretação

- k representa:
    - velocidade de crescimento;
    - intensidade da dinâmica;
    - comportamento temporal do sistema.
""")

    # --------------------------------------------------------
    # CÁLCULO DOS ks
    # --------------------------------------------------------

    k_valores = []

    for i in range(len(taxas)):
        k = taxas[i] / temperatura[i]

        k_valores.append(k)

    k_valores = np.array(k_valores)

    k_df = pd.DataFrame({

        "Temperatura": np.round(
            temperatura[:-1],
            2
        ),

        "dT/dt": np.round(
            taxas,
            4
        ),

        "k": np.round(
            k_valores,
            6
        )
    })

    # média

    k_medio = np.mean(k_valores)

    st.metric(
        "k ",
        round(k_medio, 6)
    )

    # ============================================================
    # 4. MODELO SEM OTIMIZAÇÃO
    # ============================================================

st.header("5. Modelo Matemático Sem Otimização")

col1, col2 = st.columns([1, 2])

# ------------------------------------------------------------
# ESQUERDA -> EQUAÇÃO
# ------------------------------------------------------------

with col1:
    with col1:
        st.subheader("Código Python")

        st.code('''
    T0 = temperatura[0]

    previsao_inicial = []

    for t in tempo:

        T = T0 * np.exp(k_medio * t)

        previsao_inicial.append(T)

    previsao_inicial = np.array(
        previsao_inicial
    )
    ''', language='python')


    st.subheader("Equação do Modelo")

    st.latex(
        r"T(t)=T_0e^{kt}"
    )

    st.markdown("""
Utilizando:

- temperatura inicial;
- valor médio de k.
""")

# ------------------------------------------------------------
# DIREITA -> PREVISÃO
# ------------------------------------------------------------

with col2:

    T0 = temperatura[0]

    previsao_inicial = []

    for t in tempo:
        T = T0 * np.exp(k_medio * t)

        previsao_inicial.append(T)

    previsao_inicial = np.array(
        previsao_inicial
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        tempo,
        temperatura,
        'o-',
        linewidth=3,
        label='Real'
    )

    ax.plot(
        tempo,
        previsao_inicial,
        's--',
        linewidth=3,
        label='Modelo Inicial'
    )

    ax.set_title(
        "Modelo Sem Otimização"
    )

    ax.set_xlabel("Tempo")

    ax.set_ylabel("Temperatura")

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)
    # ============================================================

# ============================================================
# 4. OTIMIZAÇÃO COM GRID SEARCH
# ============================================================

st.header("6. Otimização do Modelo")

col1, col2 = st.columns([1,2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
melhor_rmse = 999999

melhor_k = 0

for k in np.arange(
    -0.01,
    0.05,
    0.0001
):

    T0 = temperatura[0]

    previsao = []

    for t in tempo:

        T = T0*np.exp(k*t)

        previsao.append(T)

    previsao = np.array(previsao)

    rmse = np.sqrt(
        np.mean(
            (temperatura - previsao)**2
        )
    )

    if rmse < melhor_rmse:

        melhor_rmse = rmse

        melhor_k = k

        melhor_prev = previsao
''', language='python')

# ------------------------------------------------------------
# DIREITA -> RESULTADOS
# ------------------------------------------------------------

with col2:

    melhor_rmse = 999999

    melhor_k = 0

    melhor_prev = None

    for k in np.arange(
        -0.01,
        0.05,
        0.0001
    ):

        T0 = temperatura[0]

        previsao = []

        for t in tempo:

            T = T0*np.exp(k*t)

            previsao.append(T)

        previsao = np.array(previsao)

        rmse = np.sqrt(
            np.mean(
                (temperatura - previsao)**2
            )
        )

        if rmse < melhor_rmse:

            melhor_rmse = rmse

            melhor_k = k

            melhor_prev = previsao

    st.markdown("""
### Função Objetivo
""")

    st.latex(
        r"RMSE=\sqrt{\frac{1}{n}\sum(y_i-\hat y_i)^2}"
    )

    st.success(
        "✅ Melhor parâmetro encontrado!"
    )

    st.metric(
        "Melhor k",
        round(melhor_k,6)
    )

    st.metric(
        "RMSE",
        round(melhor_rmse,6)
    )

# ============================================================
# 5. REAL X PREVISTO
# ============================================================
# ============================================================
# 7. MODELO INICIAL VS OTIMIZADO
# ============================================================
# ============================================================
# 7. MODELO INICIAL VS MODELO OTIMIZADO
# ============================================================

st.header(
    "7. Comparação: Modelo Inicial vs Modelo Otimizado"
)

col1, col2 = st.columns([1,2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO PYTHON
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
fig, ax = plt.subplots(figsize=(10,5))

# dados reais

ax.plot(
    tempo,
    temperatura,
    'o-',
    linewidth=3,
    label='Dados Reais'
)

# modelo inicial

ax.plot(
    tempo,
    previsao_inicial,
    's--',
    linewidth=3,
    label='Modelo Inicial'
)

# modelo otimizado

ax.plot(
    tempo,
    melhor_prev,
    'd-.',
    linewidth=3,
    label='Modelo Otimizado'
)

ax.set_xlabel("Tempo")

ax.set_ylabel("Temperatura")

ax.set_title(
    "Comparação dos Modelos"
)

ax.grid(True)

ax.legend()

st.pyplot(fig)
''', language='python')

# ------------------------------------------------------------
# DIREITA -> EXPLICAÇÃO + GRÁFICO
# ------------------------------------------------------------

with col2:

    st.markdown("""
### Interpretação

Modelo inicial:
- utiliza o valor médio de k;
- aproximação matemática inicial.

Modelo otimizado:
- utiliza Grid Search;
- minimiza o RMSE;
- melhora o ajuste do modelo.

Objetivo:
- reduzir o erro;
- melhorar a previsão;
- aproximar o modelo dos dados reais.
""")

    st.latex(
        r"T(t)=T_0e^{kt}"
    )

    st.markdown("""
### Comparação Visual
""")

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(10,5))

    # dados reais

    ax.plot(
        tempo,
        temperatura,
        'o-',
        linewidth=3,
        label='Dados Reais'
    )

    # modelo inicial

    ax.plot(
        tempo,
        previsao_inicial,
        's--',
        linewidth=3,
        label='Modelo Inicial'
    )

    # modelo otimizado

    ax.plot(
        tempo,
        melhor_prev,
        'd-.',
        linewidth=3,
        label='Modelo Otimizado'
    )

    ax.set_xlabel("Tempo")

    ax.set_ylabel("Temperatura")

    ax.set_title(
        "Comparação entre Modelos"
    )

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)
# ============================================================
# 7. TOMADA DE DECISÃO
# ============================================================

st.header("8. Sistema Inteligente de Decisão")

col1, col2 = st.columns([1,2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
if valor < 22:

    estado = "Baixo"

elif valor < 28:

    estado = "Ideal"

elif valor < 35:

    estado = "Atenção"

else:

    estado = "Crítico"
''', language='python')

# ------------------------------------------------------------
# DIREITA -> RESULTADO
# ------------------------------------------------------------

with col2:

    analise = []

    for i in range(len(melhor_prev)):

        valor = melhor_prev[i]

        if valor < 22:

            estado = "Baixo"

            decisao = "Sem necessidade de ação"

        elif valor < 28:

            estado = "Ideal"

            decisao = "Ambiente estável"

        elif valor < 35:

            estado = "Atenção"

            decisao = "Monitorar sistema"

        else:

            estado = "Crítico"

            decisao = "Acionar resfriamento"

        analise.append([
            tempo[i],
            round(valor,2),
            estado,
            decisao
        ])

    analise_df = pd.DataFrame(
        analise,
        columns=[
            "Tempo",
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
# 8. ZONAS TÉRMICAS
# ============================================================

st.header("9. Visualização Inteligente das Zonas Térmicas")

col1, col2 = st.columns([1,2])

# ------------------------------------------------------------
# ESQUERDA -> CÓDIGO
# ------------------------------------------------------------

with col1:

    st.subheader("Código Python")

    st.code('''
ax.axhspan(0,22,color='blue')

ax.axhspan(22,28,color='green')

ax.axhspan(28,35,color='yellow')

ax.axhspan(35,50,color='red')
''', language='python')

# ------------------------------------------------------------
# DIREITA -> VISUALIZAÇÃO
# ------------------------------------------------------------

with col2:

    fig, ax = plt.subplots(figsize=(11,5))

    ax.plot(
        tempo,
        melhor_prev,
        'o-',
        linewidth=3,
        label='Temperatura Prevista'
    )

    # zonas

    ax.axhspan(
        0,
        22,
        color='blue',
        alpha=0.12,
        label='Baixo'
    )

    ax.axhspan(
        22,
        28,
        color='green',
        alpha=0.12,
        label='Ideal'
    )

    ax.axhspan(
        28,
        35,
        color='yellow',
        alpha=0.15,
        label='Atenção'
    )

    ax.axhspan(
        35,
        50,
        color='red',
        alpha=0.15,
        label='Crítico'
    )

    ax.set_xlabel("Tempo")

    ax.set_ylabel("Temperatura")

    ax.set_title(
        "Zonas Inteligentes de Temperatura"
    )

    ax.grid(True)

    handles, labels = ax.get_legend_handles_labels()

    by_label = dict(zip(labels, handles))

    ax.legend(
        by_label.values(),
        by_label.keys(),
        loc='upper left'
    )

    st.pyplot(fig)
