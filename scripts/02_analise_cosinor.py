import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import kruskal, kurtosis, shapiro, skew

# ==============================================================
# 1. CONFIGURATION AND DATA LOADING
# ==============================================================

FILE_PATH = "/content/drive/MyDrive/FEBRE AMARELA- TAUBATÉ/fa_casoshumanos_1994-2026.csv"

# Load dataset with proper encoding for Brazilian public health data
df = pd.read_csv(FILE_PATH, sep=";", encoding="latin1")
df_analise = df.copy()

# Temporal filtering (from 2008 onwards)
df_analise = df_analise[df_analise["ANO_IS"] >= 2008].copy()

# ==============================================================
# 2. STANDARDIZATION & EPIDEMIOLOGICAL MAPPINGS
# ==============================================================

mapa_uf_regiao = {
    11: ("RO", "Norte"),
    12: ("AC", "Norte"),
    13: ("AM", "Norte"),
    14: ("RR", "Norte"),
    15: ("PA", "Norte"),
    16: ("AP", "Norte"),
    17: ("TO", "Norte"),
    21: ("MA", "Nordeste"),
    22: ("PI", "Nordeste"),
    23: ("CE", "Nordeste"),
    24: ("RN", "Nordeste"),
    25: ("PB", "Nordeste"),
    26: ("PE", "Nordeste"),
    27: ("AL", "Nordeste"),
    28: ("SE", "Nordeste"),
    29: ("BA", "Nordeste"),
    31: ("MG", "Sudeste"),
    32: ("ES", "Sudeste"),
    33: ("RJ", "Sudeste"),
    35: ("SP", "Sudeste"),
    41: ("PR", "Sul"),
    42: ("SC", "Sul"),
    43: ("RS", "Sul"),
    50: ("MS", "Centro-Oeste"),
    51: ("MT", "Centro-Oeste"),
    52: ("GO", "Centro-Oeste"),
    53: ("DF", "Centro-Oeste"),
}

df_analise["COD_UF_LPI"] = pd.to_numeric(
    df_analise["COD_UF_LPI"], errors="coerce"
)
df_analise["UF_SIGLA"] = df_analise["COD_UF_LPI"].map(
    lambda x: mapa_uf_regiao.get(x, ("Ignorado", "Ignorado"))[0]
)
df_analise["REGIAO"] = df_analise["COD_UF_LPI"].map(
    lambda x: mapa_uf_regiao.get(x, ("Ignorado", "Ignorado"))[1]
)

# Date conversion and month extraction
df_analise["DT_IS"] = pd.to_datetime(
    df_analise["DT_IS"], dayfirst=True, errors="coerce"
)
df_analise["MES_IS"] = df_analise["DT_IS"].dt.month

# ==============================================================
# 3. MONTHLY TIME-SERIES RECONSTRUCTION (STATE LEVEL)
# ==============================================================

ano_min = int(df_analise["ANO_IS"].dropna().min())
ano_max = int(df_analise["ANO_IS"].dropna().max())
anos = range(ano_min, ano_max + 1)
meses = range(1, 13)
estados = sorted(df_analise["UF_LPI"].dropna().unique())

calendario = pd.MultiIndex.from_product(
    [estados, anos, meses], names=["UF_LPI", "ANO_IS", "MES_IS"]
).to_frame(index=False)

serie_mensal = (
    df_analise.groupby(["UF_LPI", "ANO_IS", "MES_IS"])
    .size()
    .reset_index(name="Casos")
)

serie_completa = calendario.merge(
    serie_mensal, on=["UF_LPI", "ANO_IS", "MES_IS"], how="left"
)
serie_completa["Casos"] = serie_completa["Casos"].fillna(0)

# ==============================================================
# 4. DESCRIPTIVE STATISTICS & NORMALITY TESTS
# ==============================================================

resultado_desc = []
resultado_shapiro = []

for uf in estados:
  dados = serie_completa[serie_completa["UF_LPI"] == uf]["Casos"]

  resultado_desc.append({
      "Estado": uf,
      "N_months": len(dados),
      "Mean": dados.mean(),
      "Median": dados.median(),
      "Std_Dev": dados.std(),
      "Min": dados.min(),
      "Max": dados.max(),
      "Skewness": skew(dados),
      "Kurtosis": kurtosis(dados),
  })

  w_val, p_val = shapiro(dados) if len(dados) >= 3 else (np.nan, np.nan)
  resultado_shapiro.append({
      "Estado": uf,
      "Shapiro_W": w_val,
      "Shapiro_p": p_val,
  })

df_desc = pd.DataFrame(resultado_desc)
df_shapiro = pd.DataFrame(resultado_shapiro)

print("\n--- Descriptive Statistics Summary ---")
print(df_desc.head())

print("\n--- Shapiro-Wilk Normality Test ---")
print(df_shapiro.head())

# Kruskal-Wallis test across states
grupos = [
    serie_completa[serie_completa["UF_LPI"] == uf]["Casos"] for uf in estados
]
h_stat, kw_p_val = kruskal(*grupos)
print(f"\nKruskal-Wallis Test across States: H = {h_stat:.3f}, p = {kw_p_val}")

# ==============================================================
# 5. COSINOR MODEL FOR CIRCANNual RHYTHMICITY
# ==============================================================


def cosinor_model(dados, periodo=12):
  dados = dados.copy()
  t = dados["MES_IS"].values - 1
  omega = 2 * np.pi / periodo

  dados["cos"] = np.cos(omega * t)
  dados["sin"] = np.sin(omega * t)

  X = sm.add_constant(dados[["cos", "sin"]])
  y = dados["Casos"]

  modelo = sm.OLS(y, X).fit()

  M = modelo.params["const"]
  beta_cos = modelo.params["cos"]
  beta_sin = modelo.params["sin"]

  amplitude = np.sqrt(beta_cos**2 + beta_sin**2)
  phi = np.arctan2(beta_sin, beta_cos)
  if phi < 0:
    phi += 2 * np.pi

  acrophase_mes = (phi * periodo / (2 * np.pi)) + 1

  return {
      "Mesor": round(M, 3),
      "Amplitude": round(amplitude, 3),
      "Acrophase_month": round(acrophase_mes, 2),
      "p_value": modelo.f_pvalue,
      "R2": round(modelo.rsquared, 4),
  }


resultados_cosinor = []
for uf, grupo in serie_completa.groupby("UF_LPI"):
  res = cosinor_model(grupo, periodo=12)
  res["Estado"] = uf
  resultados_cosinor.append(res)

df_cosinor = pd.DataFrame(resultados_cosinor)[
    ["Estado", "Mesor", "Amplitude", "Acrophase_month", "p_value", "R2"]
]

print("\n--- Cosinor Model Results ---")
print(df_cosinor.head())
