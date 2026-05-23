# E-Commerce Analyst Co-Pilot 

> An LLM-powered system that reads your business data 
> and writes the weekly analyst report automatically.

## The Problem
Every Monday, data analysts spend 2-3 hours pulling 
metrics, writing summaries, and flagging anomalies.
This project automates that entire workflow.

## What It Does
-  Ingests raw e-commerce data (orders, customers, returns)
-  Transforms it into clean weekly metrics using dbt + DuckDB
-  Uses Claude API + RAG to read metrics and generate insights
-  Auto-drafts a weekly analyst report a human just edits and sends
-  Serves everything through a live Streamlit app

## Architecture
## Tech Stack
| Layer | Tool |
|---|---|
| Data storage | DuckDB |
| Transformation | dbt |
| LLM | Claude API (Anthropic) |
| Context layer | RAG over metric definitions |
| App | Streamlit |
| Language | Python |

## Dataset
- 3,000 orders across 52 weeks (2024)
- 500 customers across 7 Indian cities
- 5 product categories
- Generated with realistic seasonality and return patterns

## Progress
- [x] Day 1 — Project setup + dataset generated
- [x] Day 2 — DuckDB + dbt pipeline (PASS=3, 53 weeks of metrics)
- [ ] Day 3 — Claude API integration + insight generation
- [ ] Day 4 — RAG layer + business context
- [ ] Day 5 — Auto report drafting + anomaly flags
- [ ] Day 6 — Streamlit app + deployment

## Results
*(updating daily as project completes)*

## How to Run
```bash
git clone https://github.com/YOUR_USERNAME/ecom-analyst-copilot
cd ecom-analyst-copilot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd dbt_project && dbt run
```

## Author
Built as a portfolio project to demonstrate end-to-end 
analytics engineering + LLM integration skills.