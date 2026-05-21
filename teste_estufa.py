# ============================================================
# SISTEMA DINÂMICO COM OTIMIZAÇÃO DE k
# ============================================================

import requests
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# firebase
import firebase_admin

from firebase_admin import credentials
from firebase_admin import db


# ============================================================
# FIREBASE
# ============================================================

if not firebase_admin._apps:

    cred = credentials.Certificate("chave_certo.json")

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://esp32-fe8e3-default-rtdb.firebaseio.com/'
    })


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
# HISTÓRICO
# ============================================================

historico_tempo = []

historico_T_real = []

historico_T_ext = []

historico_T_prev = []

historico_k = []

historico_rmse = []


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while True:

    print("\n==============================")
    print("NOVA ATUALIZAÇÃO")
    print("==============================")


    # ========================================================
    # API CLIMÁTICA
    # ========================================================

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m"
    )

    weather_data = requests.get(weather_url).json()

    current = weather_data["current"]

    T_ext = current["temperature_2m"]

    horario = current["time"]


    # ========================================================
    # FIREBASE
    # ========================================================

    ref = db.reference("/historico")

    dados = ref.get()

    ultima_chave = list(dados.keys())[-1]

    ultimo_dado = dados[ultima_chave]

    T_real = float(ultimo_dado["temperatura"])


    # ========================================================
    # ARMAZENAMENTO
    # ========================================================

    historico_tempo.append(horario)

    historico_T_real.append(T_real)

    historico_T_ext.append(T_ext)


    # ========================================================
    # GRID SEARCH
    # ========================================================

    if len(historico_T_real) >= 5:

        melhor_rmse = 999999

        melhor_k = 0

        melhor_previsoes = []

        # vários valores possíveis de k
        valores_k = np.arange(0.001, 0.1, 0.001)

        # testa todos os k
        for k in valores_k:

            previsoes = []

            # inicia modelo
            T_modelo = historico_T_real[0]

            # simulação temporal
            for i in range(len(historico_T_real)):

                T_modelo = (
                    T_modelo
                    + k * (
                        historico_T_ext[i]
                        - T_modelo
                    )
                )

                previsoes.append(T_modelo)

            previsoes = np.array(previsoes)

            # RMSE
            rmse = np.sqrt(
                np.mean(
                    (
                        np.array(historico_T_real)
                        - previsoes
                    ) ** 2
                )
            )

            # melhor solução
            if rmse < melhor_rmse:

                melhor_rmse = rmse

                melhor_k = k

                melhor_previsoes = previsoes

        # melhor previsão atual
        T_prev = melhor_previsoes[-1]

    else:

        # fase inicial
        melhor_k = 0.02

        melhor_rmse = 0

        T_prev = (
            T_real
            + melhor_k * (T_ext - T_real)
        )


    # ========================================================
    # HISTÓRICO
    # ========================================================

    historico_T_prev.append(T_prev)

    historico_k.append(melhor_k)

    historico_rmse.append(melhor_rmse)


    # ========================================================
    # SISTEMA INTELIGENTE
    # ========================================================

    if T_prev < 18:

        estado = "FRIO"

        acao = "Ligar aquecimento"

    elif T_prev < 26:

        estado = "IDEAL"

        acao = "Ambiente estável"

    elif T_prev < 32:

        estado = "QUENTE"

        acao = "Ligar ventiladores"

    else:

        estado = "CRÍTICO"

        acao = "Acionar exaustores"


    # ========================================================
    # RESULTADOS
    # ========================================================

    print(f"\nHorário: {horario}")

    print(f"Temperatura externa: {T_ext:.2f}")

    print(f"Temperatura real: {T_real:.2f}")

    print(f"Temperatura prevista: {T_prev:.2f}")

    print(f"\nMelhor k: {melhor_k:.4f}")

    print(f"RMSE: {melhor_rmse:.4f}")

    print(f"\nEstado: {estado}")

    print(f"Ação: {acao}")


    # ========================================================
    # DATAFRAME
    # ========================================================

    base = pd.DataFrame({

        "Horario": historico_tempo,

        "T_real": historico_T_real,

        "T_externa": historico_T_ext,

        "T_prevista": historico_T_prev,

        "k": historico_k,

        "RMSE": historico_rmse

    })

    print("\nBASE ATUAL\n")

    print(base.tail())


    # ========================================================
    # GRÁFICO
    # ========================================================

    plt.figure(figsize=(12,6))

    plt.plot(
        historico_T_real,
        'o-',
        linewidth=3,
        label='Temperatura Real'
    )

    plt.plot(
        historico_T_prev,
        's--',
        linewidth=3,
        label='Temperatura Prevista'
    )

    plt.plot(
        historico_T_ext,
        'd-.',
        linewidth=3,
        label='Temperatura Externa'
    )

    plt.xlabel("Tempo")

    plt.ylabel("Temperatura")

    plt.title(
        "Sistema Dinâmico Inteligente"
    )

    plt.grid(True)

    plt.legend()

    plt.show(block=False)

    plt.pause(0.1)

    plt.close()


    # ========================================================
    # ESPERA
    # ========================================================

    time.sleep(5)