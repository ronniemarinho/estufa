# ============================================================
# SISTEMA DINÂMICO INTELIGENTE DE TRANSFERÊNCIA DE CALOR
# ============================================================
#
# MODELO:
#
# dT/dt = k(T_ext - T)
#
# Aplicações:
# - Estufas
# - Biossistemas
# - Agricultura Inteligente
# - Controle térmico
# - IoT agrícola
#
# Desenvolvido por:
# Prof. Dr. Ronnie Shida Marinho
# ============================================================

# ============================================================
# BIBLIOTECAS
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests

from streamlit_autorefresh import st_autorefresh

# firebase
import firebase_admin

from firebase_admin import credentials
from firebase_admin import db


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    layout="wide",
    page_title="🌱 Sistema Inteligente de Monitoramento e Predição Térmica em Estufas Agrícolas"
)

# ============================================================
# TÍTULO
# ============================================================

st.title("🌡️Sistema Inteligente de Monitoramento e Predição Térmica em Estufas Agrícolas🌱")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "Logo_Unesp.png",
        width=650
    )


st.markdown("""
O sistema toma decisões automaticamente com base
na temperatura prevista pelo modelo matemático.
""")

regras_df = pd.DataFrame({

    "Faixa de Temperatura": [
        "< 18 °C",
        "18 °C até 26 °C",
        "26 °C até 32 °C",
        "> 32 °C"
    ],

    "Estado": [
        "FRIO",
        "IDEAL",
        "QUENTE",
        "CRÍTICO"
    ],

    "Decisão": [
        "🔥 Ligar aquecimento",
        "✅ Ambiente estável",
        "🌬️ Ligar ventilação",
        "🚨 Acionar exaustores"
    ]
})

st.dataframe(
    regras_df,
    use_container_width=True
)

st.markdown("""
## Modelagem Dinâmica da Transferência de Calor aplicada à Engenharia de Biossistemas

Sistema baseado em:

- Sensores IoT
- Firebase
- Open-Meteo API
""")

# ============================================================
# AUTO REFRESH
# ============================================================

st_autorefresh(interval=5000, key="refresh")

# ============================================================
# FIREBASE
# ============================================================

if not firebase_admin._apps:

    cred = credentials.Certificate(
    dict(st.secrets["gcp_service_account"]))

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://esp32-fe8e3-default-rtdb.firebaseio.com/'
    })

##################################################
# LER DADOS DO FIREBASE
##################################################

ref = db.reference("/historico")

dados = ref.get()
# ============================================================
# CIDADE
# ============================================================

cidade = "Tupã"

# ============================================================
# GEOCODING
# ============================================================

geo_url = (
    f"https://geocoding-api.open-meteo.com/v1/search?"
    f"name={cidade}&count=1&language=pt&format=json"
)

geo_data = requests.get(geo_url).json()

latitude = geo_data["results"][0]["latitude"]

longitude = geo_data["results"][0]["longitude"]

# ============================================================
# TEMPERATURA EXTERNA
# ============================================================

weather_url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}"
    f"&longitude={longitude}"
    f"&current=temperature_2m"
)

weather_data = requests.get(weather_url).json()

current = weather_data["current"]

T_ext = current["temperature_2m"]

horario_api = current["time"]

# ============================================================
# LEITURA FIREBASE
# ============================================================

ref = db.reference("/historico")

dados = ref.get()

lista = []

if dados:

    for chave, valor in dados.items():

        lista.append({

            "Temperatura": valor.get("temperatura"),

            "Umidade": valor.get("umidade"),

            "DataHora": valor.get("data_hora")

        })

df = pd.DataFrame(lista)

# ============================================================
# VERIFICAÇÃO
# ============================================================

if df.empty:

    st.warning("Nenhum dado encontrado.")

else:

    # ========================================================
    # TRATAMENTO
    # ========================================================

    df["DataHora"] = pd.to_datetime(
        df["DataHora"],
        format="%d/%m/%Y %H:%M:%S"
    )

    df = df.sort_values("DataHora")

    # ========================================================
    # VARIÁVEIS
    # ========================================================

    tempo_real = df["DataHora"]

    T_real = df["Temperatura"].astype(float).values

    tempo = np.arange(len(T_real))

    # ========================================================
    # CARDS
    # ========================================================

    st.header("📊 Resumo Térmico")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🌡️ Temperatura Atual",
            f"{T_real[-1]:.2f} °C"
        )

    with col2:

        st.metric(
            "🌤️ Temperatura Externa",
            f"{T_ext:.2f} °C"
        )

    with col3:

        st.metric(
            "📈 Temperatura Média",
            f"{np.mean(T_real):.2f} °C"
        )

    with col4:

        st.metric(
            "📉 Temperatura Mínima",
            f"{np.min(T_real):.2f} °C"
        )

    # ========================================================
    # MODELO MATEMÁTICO
    # ========================================================

    st.header("📘 Modelo Matemático")

    st.markdown("""
    Sistema baseado na Lei de Resfriamento de Newton.
    """)

    st.latex(
        r"\frac{dT}{dt}=k(T_{ext}-T)"
    )
    st.markdown("""
    Onde:

    - T = temperatura interna
    - T_ext = temperatura externa
    - k = coeficiente térmico
    """)

    st.subheader("Método Numérico de Euler")

    st.latex(
        r"T_{novo}=T+k(T_{ext}-T)"
    )
    # ========================================================
    # GRID SEARCH
    # ========================================================

    st.header("🧠 Otimização do Coeficiente k")

    st.markdown("""
    O sistema testa vários valores de k e escolhe o que minimiza o erro RMSE.
    """)

    melhor_rmse = 999999

    melhor_k = 0

    melhor_prev = []

    valores_k = np.arange(0.001, 0.10, 0.001)

    # ========================================================
    # TESTE DOS VALORES DE k
    # ========================================================

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

                (T_real - previsoes) ** 2

            )
        )

        if rmse < melhor_rmse:

            melhor_rmse = rmse

            melhor_k = k

            melhor_prev = previsoes

    # ========================================================
    # MÉTRICAS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🔥 Melhor k",
            round(float(melhor_k), 5)
        )

    with col2:

        st.metric(
            "📉 RMSE",
            round(float(melhor_rmse), 5)
        )

    # ========================================================
    # EQUAÇÃO RMSE
    # ========================================================

    st.subheader("Função Objetivo")

    st.latex(
        r"RMSE=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2}"
    )
    # ========================================================
    # COMPARAÇÃO
    # ========================================================

    st.header("📈 Comparação Real x Previsto")

    base_prev = pd.DataFrame({

        "Tempo": tempo_real,

        "Temperatura Real": T_real,

        "Temperatura Prevista": melhor_prev

    })

    st.dataframe(
        base_prev,
        use_container_width=True
    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=tempo_real,

            y=T_real,

            mode='lines+markers',

            name='Temperatura Real'
        )
    )

    fig.add_trace(

        go.Scatter(

            x=tempo_real,

            y=melhor_prev,

            mode='lines+markers',

            name='Temperatura Prevista'
        )
    )

    fig.update_layout(

        title="Sistema Dinâmico de Transferência de Calor",

        xaxis_title="Tempo",

        yaxis_title="Temperatura (°C)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ========================================================
    # ERRO
    # ========================================================

    st.header("📉 Análise do Erro")

    erro = T_real - melhor_prev

    erro_df = pd.DataFrame({

        "Tempo": tempo_real,

        "Erro": np.round(erro, 3)

    })

    st.dataframe(
        erro_df,
        use_container_width=True
    )

    fig2 = px.line(

        erro_df,

        x="Tempo",

        y="Erro",

        title="Erro do Modelo"

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ========================================================
    # DECISÃO INTELIGENTE
    # ========================================================

    st.header("🤖 Sistema Inteligente de Decisão")

    temperatura_atual = melhor_prev[-1]

    if temperatura_atual < 18:

        estado = "FRIO"

        decisao = "🔥 Ligar aquecimento"

        cor = "blue"

    elif temperatura_atual < 26:

        estado = "IDEAL"

        decisao = "✅ Ambiente estável"

        cor = "green"

    elif temperatura_atual < 32:

        estado = "QUENTE"

        decisao = "🌬️ Ligar ventilação"

        cor = "orange"

    else:

        estado = "CRÍTICO"

        decisao = "🚨 Acionar exaustores"

        cor = "red"

    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.header("🌱 Estado do Biossistema")

    st.sidebar.metric(
        "Temperatura Prevista",
        f"{temperatura_atual:.2f} °C"
    )

    st.sidebar.metric(
        "Melhor k",
        round(float(melhor_k), 5)
    )

    st.sidebar.metric(
        "RMSE",
        round(float(melhor_rmse), 5)
    )
    st.sidebar.header("Cidade de Tupã")
    st.sidebar.subheader("📌 Estado Atual")

    if estado == "IDEAL":

        st.sidebar.success(estado)

    elif estado == "QUENTE":

        st.sidebar.warning(estado)

    elif estado == "FRIO":

        st.sidebar.warning(estado)

    else:

        st.sidebar.error(estado)

    st.sidebar.subheader("🧠 Decisão")

    st.sidebar.info(decisao)

    # ========================================================
    # VELOCÍMETRO
    # ========================================================

    fig_gauge = go.Figure(go.Indicator(

        mode="gauge+number",

        value=float(temperatura_atual),

        title={'text': "Temperatura Prevista"},

        gauge={

            'axis': {'range': [0, 40]},

            'steps': [

                {'range': [0, 18], 'color': "blue"},

                {'range': [18, 26], 'color': "green"},

                {'range': [26, 32], 'color': "orange"},

                {'range': [32, 40], 'color': "red"}

            ]
        }
    ))

    st.sidebar.plotly_chart(
        fig_gauge,
        use_container_width=True
    )

    # ========================================================
    # INTERPRETAÇÃO
    # ========================================================

