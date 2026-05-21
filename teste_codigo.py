# ============================================================
# SISTEMA INTELIGENTE PARA IRRIGAÇÃO COM VPD
# ============================================================

# ============================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# numpy -> cálculos matemáticos
import numpy as np

# pandas -> manipulação de tabelas
import pandas as pd

# matplotlib -> geração de gráficos
import matplotlib.pyplot as plt


# ============================================================
# 1. DADOS DOS SENSORES
# ============================================================

# vetor de tempo (minutos)
tempo = np.array([0, 10, 20, 30, 40, 50])

# temperatura em graus Celsius
T = np.array([28, 29, 30, 31, 32, 33])

# umidade relativa do ar (%)
U = np.array([72, 70, 68, 65, 63, 60])

# criação do dataframe
base = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": T,
    "Umidade": U
})

# exibição da base
print("\nBASE DE DADOS\n")
print(base)


# ============================================================
# 2. CÁLCULO DO VPD
# ============================================================

# lista para armazenar os valores calculados do VPD
VPD_real = []

# percorre todos os valores de temperatura e umidade
for i in range(len(T)):

    # --------------------------------------------------------
    # cálculo da pressão de saturação do vapor (es)
    # --------------------------------------------------------
    # fórmula:
    # es = 0.6108 * exp((17.27*T)/(T+237.3))
    # --------------------------------------------------------

    es = (
        0.6108 *
        np.exp(
            (17.27 * T[i]) /
            (T[i] + 237.3)
        )
    )

    # --------------------------------------------------------
    # cálculo da pressão real de vapor (ea)
    # --------------------------------------------------------

    ea = es * (U[i] / 100)

    # --------------------------------------------------------
    # cálculo do VPD
    # --------------------------------------------------------
    # VPD = es - ea
    # --------------------------------------------------------

    vpd = es - ea

    # adiciona o valor calculado na lista
    VPD_real.append(vpd)

# converte a lista para vetor numpy
VPD_real = np.array(VPD_real)

# dataframe com os resultados
base_vpd = pd.DataFrame({
    "Tempo": tempo,
    "Temperatura": T,
    "Umidade": U,
    "VPD": np.round(VPD_real, 3)
})

# exibição da tabela
print("\nRESULTADOS DO VPD\n")
print(base_vpd)


# ============================================================
# 3. GRÁFICO DO VPD REAL
# ============================================================

plt.figure(figsize=(10, 5))

# gráfico da evolução temporal do VPD
plt.plot(
    tempo,
    VPD_real,
    'o-',
    linewidth=3,
    label='VPD Real'
)

# títulos e labels
plt.xlabel("Tempo")
plt.ylabel("VPD")
plt.title("Evolução Temporal do VPD")

# grade
plt.grid(True)

# legenda
plt.legend()

# exibição
plt.show()


# ============================================================
# 4. SISTEMA DINÂMICO
# ============================================================

# o modelo matemático utilizado é:
#
# dV/dt = kV
#
# solução:
#
# V(t) = V0 * exp(k*t)
#
# onde:
# V0 -> valor inicial do VPD
# k  -> taxa de crescimento


# ============================================================
# 5. GRID SEARCH PARA ENCONTRAR O MELHOR k
# ============================================================

# variável com erro inicial muito alto
melhor_rmse = 999999

# melhor valor de k
melhor_k = 0

# melhor previsão encontrada
melhor_prev = None

# vários valores possíveis para k
valores_k = np.arange(-0.05, 0.20, 0.0005)

# percorre todos os valores de k
for k in valores_k:

    # valor inicial do VPD
    V0 = VPD_real[0]

    # lista para armazenar previsões
    VPD_prev = []

    # calcula o VPD previsto para cada instante
    for t in tempo:

        # solução da EDO
        V = V0 * np.exp(k * t)

        # armazena previsão
        VPD_prev.append(V)

    # converte para vetor numpy
    VPD_prev = np.array(VPD_prev)

    # --------------------------------------------------------
    # cálculo do RMSE
    # --------------------------------------------------------
    # mede a diferença entre:
    # - valores reais
    # - valores previstos
    # --------------------------------------------------------

    rmse = np.sqrt(
        np.mean(
            (VPD_real - VPD_prev) ** 2
        )
    )

    # verifica se encontrou um erro menor
    if rmse < melhor_rmse:

        # atualiza o melhor erro
        melhor_rmse = rmse

        # salva o melhor k
        melhor_k = k

        # salva a melhor previsão
        melhor_prev = VPD_prev


# ============================================================
# 6. RESULTADOS DA OTIMIZAÇÃO
# ============================================================

print("\nRESULTADOS DO GRID SEARCH\n")

print(f"Melhor k encontrado: {melhor_k:.6f}")

print(f"Melhor RMSE: {melhor_rmse:.6f}")


# ============================================================
# 7. COMPARAÇÃO ENTRE REAL E PREVISTO
# ============================================================

plt.figure(figsize=(10, 5))

# curva real
plt.plot(
    tempo,
    VPD_real,
    'o-',
    linewidth=3,
    label='VPD Real'
)

# curva prevista
plt.plot(
    tempo,
    melhor_prev,
    's--',
    linewidth=3,
    label='VPD Previsto'
)

# labels
plt.xlabel("Tempo")
plt.ylabel("VPD")

# título
plt.title("Comparação entre VPD Real e Previsto")

# legenda
plt.legend()

# grade
plt.grid(True)

# exibição
plt.show()


# ============================================================
# 8. ANÁLISE DO ERRO
# ============================================================

# erro entre valor real e previsto
erro = VPD_real - melhor_prev

# dataframe do erro
erro_df = pd.DataFrame({
    "Tempo": tempo,
    "Erro": np.round(erro, 4)
})

print("\nANÁLISE DO ERRO\n")
print(erro_df)


# ============================================================
# 9. SISTEMA INTELIGENTE DE TOMADA DE DECISÃO
# ============================================================

# lista que armazenará as análises
analise = []

# percorre todas as previsões
for i in range(len(melhor_prev)):

    # valor previsto atual
    valor = melhor_prev[i]

    # --------------------------------------------------------
    # classificação do ambiente
    # --------------------------------------------------------

    if valor < 0.8:

        estado = "Muito Úmido"

        decisao = "Irrigação desnecessária"

    elif valor < 1.2:

        estado = "Ideal"

        decisao = "Ambiente estável"

    elif valor < 1.6:

        estado = "Atenção"

        decisao = "Monitorar ambiente"

    elif valor < 2.0:

        estado = "Moderado"

        decisao = "Irrigação recomendada"

    else:

        estado = "Crítico"

        decisao = "Irrigação urgente"

    # adiciona os resultados na lista
    analise.append([
        tempo[i],
        round(valor, 2),
        estado,
        decisao
    ])

# criação do dataframe final
analise_df = pd.DataFrame(
    analise,
    columns=[
        "Tempo",
        "VPD Previsto",
        "Estado",
        "Decisão"
    ]
)

# exibe resultados
print("\nANÁLISE INTELIGENTE\n")
print(analise_df)


# ============================================================
# 10. VISUALIZAÇÃO DAS ZONAS DE IRRIGAÇÃO
# ============================================================

plt.figure(figsize=(11, 5))

# curva prevista
plt.plot(
    tempo,
    melhor_prev,
    'o-',
    linewidth=3,
    label='VPD Previsto'
)

# ------------------------------------------------------------
# zonas ambientais
# ------------------------------------------------------------

# muito úmido
plt.axhspan(
    0,
    0.8,
    color='blue',
    alpha=0.12,
    label='Muito Úmido'
)

# ideal
plt.axhspan(
    0.8,
    1.2,
    color='green',
    alpha=0.12,
    label='Ideal'
)

# atenção
plt.axhspan(
    1.2,
    1.6,
    color='yellow',
    alpha=0.15,
    label='Atenção'
)

# moderado
plt.axhspan(
    1.6,
    2.0,
    color='orange',
    alpha=0.15,
    label='Moderado'
)

# crítico
plt.axhspan(
    2.0,
    5,
    color='red',
    alpha=0.15,
    label='Crítico'
)

# labels
plt.xlabel("Tempo")

plt.ylabel("VPD")

# título
plt.title("Zonas Inteligentes de Irrigação")

# grade
plt.grid(True)

# remove legendas repetidas
handles, labels = plt.gca().get_legend_handles_labels()

by_label = dict(zip(labels, handles))

plt.legend(
    by_label.values(),
    by_label.keys(),
    loc='upper left'
)

# exibe gráfico
plt.show()