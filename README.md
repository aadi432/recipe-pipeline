# 🍽️ Recipe Analytics Pipeline (Firebase + Python)  
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?logo=firebase)
![ETL](https://img.shields.io/badge/Pipeline-ETL-green)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

An end-to-end **Data Engineering pipeline** that takes semi-structured recipe data from **Firebase Firestore**, converts it into **clean analytical tables**, applies **data quality checks**, and generates **insights & charts** — all automated via Python with logging and retry logic.

This project is designed as a **professional Data Engineering assignment / portfolio project**.

---

## 📚 Table of Contents

1. [Project Overview](#-project-overview)  
2. [Architecture & Folder Structure](#-architecture--folder-structure)  
3. [Data Model (ER Diagrams)](#-data-model-erd-diagrams)  
4. [Tech Stack](#-tech-stack)  
5. [Pipeline Stages](#-pipeline-stages)  
6. [Data Quality & Validation](#-data-quality--validation)  
7. [Analytics & Outputs](#-analytics--outputs)  
8. [Orchestration](#-orchestration)  
9. [Setup & How to Run](#-setup--how-to-run)  
10. [Limitations & Future Improvements](#-limitations--future-improvements)  
11. [Conclusion](#-conclusion)  

---

## 🎯 Project Overview

This project demonstrates a realistic **Data Engineering workflow**:

- ✅ Ingest a **primary real recipe** (Pav Bhaji) + synthetic recipes into Firestore  
- ✅ Export Firestore data into **tabular CSVs**  
- ✅ Transform and clean the data for analytics  
- ✅ Validate data quality with a **custom Great-Expectations-style validator**  
- ✅ Compute metrics like complexity & engagement scores  
- ✅ Generate charts and summary insights  
- ✅ Run the entire pipeline with a **single command**  

Primary real-world recipe used: **Pav Bhaji** (from `seed_data.json`) – this is the main dataset provided by the candidate.

---

## 🏗️ Architecture & Folder Structure

```bash
recipe-pipeline/
│
├── analysis/                  # Charts & analytics summaries
│   ├── *.png                  # Visualization images
│   └── insights_summary.txt   # Text summary of key findings
│
├── outputs/
│   ├── recipe.csv             # Raw exported tables from Firestore
│   ├── ingredients.csv
│   ├── steps.csv
│   ├── users.csv
│   ├── interactions.csv
│   ├── clean/                 # Cleaned & normalized CSVs
│   │   ├── recipes_clean.csv
│   │   ├── ingredients_clean.csv
│   │   ├── steps_clean.csv
│   │   ├── users_clean.csv
│   │   └── interactions_clean.csv
│   └── validated/             # Data quality reports
│       ├── validation_report.txt
│       └── custom_ge_report.txt
│
├── scripts/
│   ├── 1_setup_firestore.py           # Seed + synthetic data into Firestore
│   ├── 2_export_firestore.py          # Export Firestore -> CSV
│   ├── 3_transform_to_csv.py          # Transform & clean CSVs
│   ├── 4_validate_csv.py              # Basic validation
│   ├── 4a_custom_expectations_check.py# GE-style data-quality checks
│   ├── 5_analytics.py                 # Charts & metrics
│   └── run_pipeline.py                # Orchestration entrypoint
│
├── seed_data.json             # Pav Bhaji primary recipe
├── serviceAccount.json        # Firebase service account (ignored in git)
├── .env                       # Env variables (paths, secrets)
├── .gitignore
├── requirements.txt
└── README.md
