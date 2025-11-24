# 🍽️ Recipe Analytics Pipeline (Firebase → Python → Analytics)

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

recipe-pipeline/
│── analysis/ # Generated charts + insights
│── exports/ # Raw JSON exports from Firestore
│── outputs/
│ ├── clean/ # Normalized cleaned CSVs
│ └── validated/ # Validation reports
│── scripts/ # ETL, validation, analytics, orchestration scripts
│── seed_data.json # Primary Pav Bhaji recipe
│── serviceAccount.json # Firebase authentication key (ignored via .gitignore)
│── .env # Secret environment variables
│── requirements.txt
│── README.md

yaml
Copy code

---

# 🧠 2. Project Overview

This pipeline executes an end-to-end workflow:

1️⃣ Insert seed + synthetic recipe data into **Firebase Firestore**  
2️⃣ Export Firestore → **JSON**  
3️⃣ Normalize JSON → **clean CSV datasets**  
4️⃣ Validate CSVs using a **custom Great-Expectations style validator**  
5️⃣ Run analytics and generate **11+ charts**  
6️⃣ Fully orchestrated with **run_pipeline.py**

This simulates a real-world Data Engineering solution using a mix of NoSQL + relational modeling.

---

# 🧩 3. Data Model (ER Diagram)

The project uses **two data models**:

---

## 🔷 3.1 Firestore ERD (Nested NoSQL Model)

┌──────────────────────────────┐
│ RECIPES │
│ id, title, desc, times, ... │
│ ingredients: [ {name, qty} ] │
│ steps: [ {order, text} ] │
└───────────────┬──────────────┘
│ 1-to-many
▼
┌────────────────────────┐
│ INTERACTIONS │
│ recipe_id, user_id │
│ type, rating, timestamp│
└────────────┬───────────┘
│ many-to-1
▼
┌──────────────────────┐
│ USERS │
│ id, name │
└──────────────────────┘

yaml
Copy code

### Relationships
- Recipe → Ingredients = **1:N**  
- Recipe → Steps = **1:N**  
- Recipe → Interactions = **1:N**  
- User → Interactions = **1:N**

---

## 🔷 3.2 CSV / Analytics ERD (Flattened Relational)

RECIPES_CLEAN ───┬───< INGREDIENTS_CLEAN
├───< STEPS_CLEAN
└───< INTERACTIONS_CLEAN >── USERS_CLEAN

yaml
Copy code

Used for analytics & reporting.

---

# 🍛 4. Primary Dataset (Your Recipe)

### 🟢 Primary real recipe: **Pav Bhaji**

This satisfies the assignment requirement to include one **real recipe created by the candidate**.

Included fields:
- Ingredients (with quantities)
- Step-by-step instructions
- Time & difficulty
- Cuisine, region, tags

Stored in `seed_data.json`.

### 🟡 Synthetic Data (Auto-generated)
- **19 vegetarian recipes**
- **10 sample Indian users**
- **120+ interactions** (view/like/cook_attempt)

---

# ⚙️ 5. ETL / ELT Pipeline Steps

## 🔹 Step 1 — Firestore Setup
Script: `1_setup_firestore.py`

- Loads Pav Bhaji (primary recipe)
- Generates 19 synthetic recipes
- Creates users
- Creates interactions
- Includes **retry logic + logging**

---

## 🔹 Step 2 — Export Firestore → JSON
Script: `2_export_firestore.py`

Exports:
exports/recipes.json
exports/users.json
exports/interactions.json

yaml
Copy code

---

## 🔹 Step 3 — Transform JSON → Clean CSVs
Script: `3_transform_to_csv.py`

Outputs:
outputs/clean/recipes_clean.csv
outputs/clean/ingredients_clean.csv
outputs/clean/steps_clean.csv
outputs/clean/users_clean.csv
outputs/clean/interactions_clean.csv

yaml
Copy code

Includes:
- Flattening nested arrays  
- Normalization  
- Retry-safe reading  

---

## 🔹 Step 4 — Data Validation (Custom GE-Style)
Script: `4_validate_csv.py`  
AND  
Script: `4a_custom_expectations_check.py` (Great-Expectations style)

Validates:
- Required columns  
- Unique IDs  
- No NULLs in key fields  
- Integer columns valid  
- Foreign keys valid  
- Step order valid  

Output:
outputs/validated/validation_report.txt
outputs/validated/custom_ge_report.txt

yaml
Copy code

---

## 🔹 Step 5 — Analytics & Visualizations
Script: `5_analytics.py`

Generates 10+ charts:
- Top ingredients  
- Difficulty distribution  
- Prep vs likes correlation  
- Top viewed recipes  
- Step count distribution  
- Top engaged recipes  
- Most active users  
- Complexity score distribution  
- Engagement score analysis  
- Etc.

Saved to:
analysis/*.png
analysis/insights_summary.txt

yaml
Copy code

---

# 🔁 6. Pipeline Orchestration

Script: `run_pipeline.py`

Runs all steps in the correct order:

python scripts/run_pipeline.py

yaml
Copy code

Includes:
- Error boundaries  
- Logging  
- Full automation  

---

# ✔️ 7. Data Quality Rules Summary

### 🟦 Recipes
- id, title required  
- Difficulty ∈ {easy, medium, hard}  
- prep/cook times ≥ 0  
- No missing timestamps  

### 🟩 Ingredients
- recipe_id required  
- ingredient_name required  

### 🟨 Steps
- recipe_id required  
- step order ≥ 1  
- sequential per recipe  

### 🟧 Users
- id unique  
- name not null  

### 🟥 Interactions
- recipe_id + user_id must reference valid tables  
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
- Ingredient frequency in high-engagement recipes  
- Most active 20 users  
- Complexity score analysis  

All charts saved under `analysis/`.

---

# ▶️ 9. How to Run the Pipeline

### Install dependencies:
```bash
pip install -r requirements.txt
Add Firebase Secret Key
Place your:

pgsql
Copy code
serviceAccount.json
in the project root.

Add .env file:
ini
Copy code
SERVICE_ACCOUNT_PATH=serviceAccount.json
PAV_SEED_PATH=seed_data.json
Run the full pipeline:
bash
Copy code
python scripts/run_pipeline.py
⚠️ 10. Limitations
Synthetic recipe descriptions are random

Ratings partially random

Requires correct Firebase config

Focused on vegetarian recipes only

🎯 11. What This Submission Demonstrates
End-to-end Data Engineering pipeline

ETL + data modeling

Semi-structured → structured transformation

Data quality checks

Analytical model creation

Visualization engineering

Retry logic + error handling

Orchestration (one-click pipeline)

📘 Conclusion
This project shows a complete academic-style Data Engineering solution, transforming raw Firestore (NoSQL) data into clean, validated, analytics-ready tables. It includes modeling, validation, visualizations, and orchestration, making it suitable for real-world pipelines and technical assignments.

🙌 Author
Aditya Shukla
