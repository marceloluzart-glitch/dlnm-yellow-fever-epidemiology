# Spatial-Temporal Modeling of Yellow Fever in Brazil: Descriptive Diagnostics and Non-Linear Lagged DLNM Pipeline (1994–2026)
## Modelagem Espaço-Temporal da Febre Amarela no Brasil: Diagnóstico Descritivo, Análise Circanual e Pipeline Inferencial DLNM (1994–2026)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Statistical Framework](https://img.shields.io/badge/stats-DLNM%20%7C%20GLM%20%7C%20HAC-green.svg)](https://www.statsmodels.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/mit-license)

---

### English Version

#### Abstract & Overview
This repository hosts a robust two-stage analytical pipeline designed to investigate the spatio-temporal dynamics and environmental drivers of human Yellow Fever across Brazilian states over a three-decade historical series (1994–2026). The project bridges descriptive data diagnostics with advanced inferential modeling, integrating **Distributed Lag Non-Linear Models (DLNM)**, Generalized Linear Models (GLMs), and **circannual rhythmic decomposition** to evaluate delayed, non-linear climatic effects modulated by immunological barriers, socio-structural vulnerabilities, and healthcare response capacity.

#### Repository Architecture
```text
├── scripts/
│   ├── 01_diagnostico_inspecao.py      # Stage 1: Raw data ingestion, schema validation, and descriptive inspection
│   └── 02_pipeline_dlnm.py             # Stage 2: Core inferential engine (Cross-basis DLNM + GLM + HAC + AF)
├── data/                               # Directory designated for raw and curated data layers
├── outputs/                            # Consolidated statistical tables, coefficients, and artifacts
└── README.md
