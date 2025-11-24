# 🍽️ Recipe Analytics Pipeline (Firebase → Python → Analytics)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?logo=firebase)
![ETL](https://img.shields.io/badge/Pipeline-ETL-green)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

---

A complete **Data Engineering pipeline** built for transforming **NoSQL Firestore recipe data** into **validated, analytical datasets** with visual insights.

This project demonstrates:

- Firestore data ingestion  
- JSON export  
- Data normalization to CSV  
- Data validation (custom Great-Expectations style)  
- Analytics & visualizations  
- Retry logic & logging  
- Orchestration via a single pipeline runner  
- Dual data model (Firestore nested + CSV relational)

---

# 📁 1. Folder Structure

```
recipe-pipeline/
│── analysis/                # Generated charts + insights
│── exports/                 # Raw JSON exports from Firestore
│── outputs/
│     ├── clean/             # Normalized cleaned CSVs
│     └── validated/         # Validation reports
│── scripts/                 # ETL, validation, analytics, orchestration scripts
│── seed_data.json           # Primary Pav Bhaji recipe
│── serviceAccount.json      # Firebase authentication key (ignored via .gitignore)
│── .env                     # Secret environment variables
│── requirements.txt
│── README.md
```

---

# 🧠 2. Project Overview

This pipeline executes an end-to-end workflow:

1️⃣ Insert seed + synthetic recipe data into **Firebase Firestore**  
2️⃣ Export Firestore → **JSON**  
3️⃣ Normalize JSON → **clean CSV datasets**  
4️⃣ Validate CSVs using a **custom Great-Expectations style validator**  
5️⃣ Run analytics and generate **11+ charts**  
6️⃣ Fully orchestrated with **run_pipeline.py**

---

# 🧩 3. Data Model (ER Diagram)

## 🔷 3.1 Firestore ERD (Nested NoSQL Model)

```
┌────────────────────────────────────┐
│               RECIPES              │
│────────────────────────────────────│
│ id                                 │
│ title                              │
│ description                        │
│ prep_time_minutes                  │
│ cook_time_minutes                  │
│ difficulty                         │
│ cuisine                            │
│ region                             │
│ created_at                         │
│ ingredients: [ { name, quantity } ]│
│ steps:       [ { order, text } ]   │
└───────────────────┬────────────────┘
                    │ 1-to-many
                    ▼
        ┌────────────────────────────────┐
        │           INTERACTIONS         │
        │────────────────────────────────│
        │ id                             │
        │ recipe_id (FK → RECIPES.id)    │
        │ user_id   (FK → USERS.id)      │
        │ type  (view / like / attempt)  │
        │ rating                         │
        │ timestamp                      │
        └───────────────────┬────────────┘
                            │ many-to-1
                            ▼
                ┌─────────────────────────────┐
                │             USERS            │
                │─────────────────────────────│
                │ id                           │
                │ name                         │
                └─────────────────────────────┘
```

---

## 🔷 3.2 CSV / Analytics ERD (Flattened Relational)

```
               ┌────────────────────────────────┐
               │          RECIPES_CLEAN         │
               │────────────────────────────────│
               │ id (PK)                        │
               │ title                          │
               │ prep_time_minutes              │
               │ cook_time_minutes              │
               │ total_time                     │
               │ difficulty                     │
               │ complexity_score               │
               │ engagement_score               │
               └───────────────┬────────────────┘
                               │ 1-to-many
               ┌───────────────┴─────────────────────┐
               ▼                                       ▼
┌──────────────────────────────┐       ┌────────────────────────────────┐
│      INGREDIENTS_CLEAN       │       │          STEPS_CLEAN           │
│──────────────────────────────│       │────────────────────────────────│
│ recipe_id (FK → RECIPES.id)  │       │ recipe_id (FK → RECIPES.id)    │
│ ingredient_name              │       │ order                          │
│ quantity                     │       │ step_text                      │
└──────────────────────────────┘       └────────────────────────────────┘

                               │ 1-to-many
                               ▼

                      ┌──────────────────────────────────┐
                      │       INTERACTIONS_CLEAN         │
                      │──────────────────────────────────│
                      │ id (PK)                          │
                      │ recipe_id (FK → RECIPES.id)      │
                      │ user_id (FK → USERS.id)          │
                      │ type                             │
                      │ timestamp                        │
                      │ rating                           │
                      └───────────────────┬────────────────┘
                                          │ many-to-1
                                          ▼
                               ┌───────────────────────────────┐
                               │          USERS_CLEAN           │
                               │───────────────────────────────│
                               │ id (PK)                       │
                               │ name                          │
                               └───────────────────────────────┘
```

---

# 🍛 4. Primary Dataset (Your Recipe)

### 🟢 Pav Bhaji (Primary Dataset)
- Real recipe provided by the candidate
- Full ingredients & steps
- Difficulty, time, tags, cuisine, region

### 🟡 Synthetic Data
- 19 vegetarian recipes  
- 10 users  
- 120+ interactions  

---

# ⚙️ 5. ETL / ELT Pipeline Steps

## Step 1 — Insert Data into Firestore  
`1_setup_firestore.py`

## Step 2 — Export Firestore → JSON  
`2_export_firestore.py`

## Step 3 — Transform JSON → Clean CSV  
`3_transform_to_csv.py`

## Step 4 — Validate CSVs  
`4_validate_csv.py`  
`4a_custom_expectations_check.py`

## Step 5 — Analytics & Visualizations  
`5_analytics.py`

---

# 🔁 6. Pipeline Orchestration

Script: `run_pipeline.py`

Runs all steps in the correct order:

```bash
python scripts/run_pipeline.py
```

---

# ✔️ 7. Data Quality Rules Summary

### 🟦 Recipes
- id, title required  
- Difficulty ∈ {easy, medium, hard}  
- prep/cook times ≥ 0  

### 🟩 Ingredients
- recipe_id required  
- ingredient_name required  

### 🟨 Steps
- step order ≥ 1  
- Sequential per recipe  

### 🟧 Users
- id unique  
- name not null  

### 🟥 Interactions
- type ∈ {view, like, cook_attempt}  
- rating ∈ {1–5 or null}

---

# 📊 8. Sample Insights Generated

- Most frequent ingredients  
- Top 10 most viewed recipes  
- Difficulty distribution  
- Prep time vs likes correlation  
- Step count analysis  
- Engagement score ranking  

---

# ▶️ 9. How to Run the Pipeline

Install dependencies:
```bash
pip install -r requirements.txt
```

Add secret keys:
```
SERVICE_ACCOUNT_PATH=serviceAccount.json
PAV_SEED_PATH=seed_data.json
```

Run:
```bash
python scripts/run_pipeline.py
```

---

⚠️ 10. Limitations
Synthetic recipe descriptions are random

Ratings partially random

Requires correct Firebase configuration

Focused on vegetarian recipes

---

🎯 11. What This Submission Demonstrates
Complete end-to-end Data Engineering pipeline

ETL + data modeling

Semi-structured → structured transformation

Data quality & validation framework

Analytical model creation

Visualization engineering

Retry logic + logging

Pipeline orchestration

---

👨‍💻 12. Author
Aditya Shukla




