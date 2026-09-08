# Spatial-Temporal Modeling of Yellow Fever in Brazil: Non-Linear Lagged Environmental Effects and Vulnerability Axes (1994–2026)
## Modelagem Espaço-Temporal da Febre Amarela no Brasil: Efeitos Não-Lineares de Defasagem Ambiental e Eixos de Vulnerabilidade (1994–2026)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Statistical Framework](https://img.shields.io/badge/stats-DLNM%20%7C%20GLM%20%7C%20HAC-green.svg)](https://www.statsmodels.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/mit-license)

---

### English Version

#### Abstract & Overview
This repository hosts the algorithmic and statistical pipeline developed to investigate the spatio-temporal transmission dynamics of human Yellow Fever across Brazilian states over a three-decade historical series (1994–2026). The analytical architecture couples **Distributed Lag Non-Linear Models (DLNM)** with Generalized Linear Models (GLMs) to quantify non-linear and delayed environmental influences while rigorously controlling for immunological barriers, socio-structural inequalities (Social Vulnerability Index - IVS), and municipal healthcare response capacity (SUS).

#### Repository Architecture
```text
├── scripts/
│   ├── 01_diagnostico_inspecao.py      # Raw data validation, schema alignment, and preprocessing
│   └── 02_pipeline_dlnm.py             # Core analytical engine (Cross-basis DLNM + GLM + HAC)
├── data/                               # Directory designated for raw and curated data layers
├── outputs/                            # Consolidated statistical tables, coefficients, and artifacts
└── README.md
