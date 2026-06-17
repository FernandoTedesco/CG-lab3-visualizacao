# Visualização: evolução da matriz elétrica do Brasil (2000-2024).
#
# Dataset: Our World in Data — Energy data (owid-energy-data.csv).
# Fonte original: https://github.com/owid/energy-data
#
# A visualização é um stacked area chart (100%) das participações de cada
# fonte na geração elétrica brasileira. A conclusão demonstrada é que a
# queda da participação da hidrelétrica (~87% -> ~55%) foi compensada
# principalmente pela ascensão combinada de eólica + solar (~0% -> ~24%),
# não por combustíveis fósseis.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# --- Carregar dados ---
URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
df = pd.read_csv(URL)
br = df[(df["country"] == "Brazil") & (df["year"].between(2000, 2024))].copy()

# Ordem de empilhamento (de baixo para cima) e cores
fontes = [
    ("hydro_share_elec",   "Hidrelétrica",    "#1f6dad"),
    ("wind_share_elec",    "Eólica",          "#5fb3a3"),
    ("solar_share_elec",   "Solar",           "#f3c14b"),
    ("biofuel_share_elec", "Biocombustíveis", "#7aa64a"),
    ("nuclear_share_elec", "Nuclear",         "#9b6fbf"),
    ("gas_share_elec",     "Gás natural",     "#bdbdbd"),
    ("oil_share_elec",     "Petróleo",        "#8c6a4a"),
    ("coal_share_elec",    "Carvão",          "#444444"),
]

x = br["year"].to_numpy()
y = [br[col].fillna(0).to_numpy() for col, _, _ in fontes]
rotulos = [r for _, r, _ in fontes]
cores   = [c for _, _, c in fontes]

# --- Figura ---
fig, ax = plt.subplots(figsize=(11, 6.2))

ax.stackplot(x, y, labels=rotulos, colors=cores, edgecolor="white", linewidth=0.3)

ax.set_xlim(2000, 2024)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_xlabel("Ano")
ax.set_ylabel("Participação na geração elétrica")
ax.set_title(
    "Matriz elétrica do Brasil",
    fontsize=14, fontweight="bold", loc="left"
)
ax.set_xticks(range(2000, 2025, 4))

# Grid sutil
ax.grid(axis="y", linestyle=":", linewidth=0.6, color="white", alpha=0.7)
ax.set_axisbelow(False)

# Legenda fora do gráfico (à direita)
ax.legend(
    loc="center left", bbox_to_anchor=(1.01, 0.5),
    frameon=False, fontsize=10, title="Fonte"
)

# --- Anotações ---
# Calcular soma solar+eólica nos extremos para a anotação
ano_ini, ano_fim = 2000, 2024
se_ini = br.loc[br.year == ano_ini, ["wind_share_elec", "solar_share_elec"]].sum(axis=1).values[0]
se_fim = br.loc[br.year == ano_fim, ["wind_share_elec", "solar_share_elec"]].sum(axis=1).values[0]
hidro_ini = br.loc[br.year == ano_ini, "hydro_share_elec"].values[0]
hidro_fim = br.loc[br.year == ano_fim, "hydro_share_elec"].values[0]

# Anotação 1: hidrelétrica encolheu (texto dentro da própria faixa azul)
ax.annotate(
    f"Hidrelétrica\n{hidro_ini:.0f}% → {hidro_fim:.0f}%",
    xy=(2012, 30), xytext=(2012, 30),
    fontsize=11, color="white", fontweight="bold",
    ha="center", va="center"
)

# Anotação 2: solar+eólica explodiu — apontando para a faixa correta
# A faixa eólica+solar em 2024 vai de ~55% (topo hidro) até ~80% (topo solar)
ax.annotate(
    f"Eólica + Solar\n{se_ini:.0f}% → {se_fim:.0f}%",
    xy=(2023.5, 68), xytext=(2010, 92),
    fontsize=11, color="#1a1a1a", fontweight="bold",
    ha="center",
    arrowprops=dict(arrowstyle="->", color="#1a1a1a", linewidth=1.2,
                    connectionstyle="arc3,rad=0.2")
)

# Subtítulo / fonte
fig.text(
    0.012, 0.005,
    "Fonte: Our World in Data — Energy data (https://github.com/owid/energy-data). Período: 2000–2024.",
    fontsize=8.5, color="#555555"
)

plt.tight_layout(rect=(0, 0.02, 1, 1))

# --- Salvar ---
plt.savefig("vis-matriz-eletrica-br.svg", bbox_inches="tight")
plt.savefig("vis-matriz-eletrica-br.png", dpi=160, bbox_inches="tight")
print("Salvo: vis-matriz-eletrica-br.svg e vis-matriz-eletrica-br.png")
