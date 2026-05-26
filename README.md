# E-Commerce Analyst Co-Pilot 🤖

> An LLM-powered system that reads your business data 
> and writes the weekly analyst report automatically.

## The Problem
Every Monday, data analysts spend 2-3 hours pulling 
metrics, writing summaries, and flagging anomalies.
This project automates that entire workflow.

## What It Does
-  Ingests raw e-commerce data (orders, customers, returns)
-  Transforms it into clean weekly metrics using dbt + DuckDB
-  Uses Groq (Llama 3.3) + RAG to read metrics and generate insights
-  Auto-detects anomalies using rule-based thresholds
-  Auto-drafts weekly analyst insights a human just edits and sends
- Serves everything through a live 3-page Streamlit app

## Live Demo
🔗  https://ecom-analyst-copilot-btgogthe3iv4ekzmn3moan.streamlit.app/

## Architecture
Raw CSVs → DuckDB → dbt models → weekly_metrics table
↓
Groq LLM + RAG context
(business definitions)
↓
Auto-drafted weekly insights
+ anomaly detection + flags
↓
3-page Streamlit app (live)
Weekly Dashboard | AI Report | Anomaly Explorer
## Tech Stack
| Layer | Tool |
|---|---|
| Data storage | DuckDB |
| Transformation | dbt (PASS=3) |
| LLM | Groq API (Llama 3.3) |
| Context layer | RAG over metric definitions |
| Anomaly detection | Rule-based thresholds |
| App | Streamlit |
| Language | Python |

## Dataset
- 3,000 orders across 53 weeks (2024)
- 500 customers across 7 Indian cities
- 5 product categories
- Generated with realistic seasonality and return patterns

## Results
-  53 weeks of clean metrics built via dbt pipeline
-  8 anomalies auto-detected (revenue drops, return spikes)
-  LLM generates 3-sentence analyst insight per week
-  Live 3-page Streamlit dashboard deployed

## Progress
- [x] Day 1 — Project setup + 3,000 row dataset generated
- [x] Day 2 — DuckDB + dbt pipeline (PASS=3, 53 weeks of metrics)
- [x] Day 3 — Groq LLM + RAG generating analyst insights — 8 anomalies auto-detected
- [x] Day 4 — 3-page Streamlit app built (Dashboard + AI Report + Anomaly Explorer)
- [x] Day 5 — Deployed live on Streamlit Cloud

## How to Run
```bash
git clone https://github.com/YOUR_USERNAME/ecom-analyst-copilot
cd ecom-analyst-copilot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd dbt_project && dbt run
cd .. && streamlit run app/main.py
```

## What the App Shows
- **Weekly Dashboard** — revenue trend, return rate, WoW growth, top category
- **AI Report** — LLM-generated analyst insight per week with anomaly flags
- **Anomaly Explorer** — all 8 anomaly weeks with expandable AI insights

## Author
Built as a portfolio project demonstrating end-to-end 
analytics engineering + LLM integration skills.