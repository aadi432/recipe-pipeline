🚀 Recipe Analytics Pipeline (Firebase + Python)

This repository contains a complete end-to-end Data Engineering pipeline that ingests recipe data from Firestore, transforms it into structured analytical tables, validates data quality using custom Great-Expectations-style rules, and generates insights through visualization and statistics.

This project simulates a real-world Data Engineering assignment with:

NoSQL → Structured ETL

Retry logic

Validation

Analytics

Orchestration

Secure secrets

ERD diagrams

Clean folder structure

📌 1. Project Overview

This pipeline performs the following:

✔ Ingests seed + synthetic recipe data into Firestore

Including a primary real dataset: Pav Bhaji.

✔ Exports Firestore collections to JSON
✔ Transforms JSON to normalized CSV tables

Using professional flattening (ingredients & steps extracted properly).

✔ Validates cleaned CSVs

Using:

Built-in validation

Custom GE-style validator (Python 3.14 compatible)

✔ Generates analytics & charts
✔ Runs end-to-end using one command

python scripts/run_pipeline.py

📁 2. Folder Structure
recipe-pipeline/
│── analysis/                # Charts + insight summaries
│── exports/                 # Raw Firestore JSON exports
│── outputs/
│     ├── clean/             # Cleaned normalized CSVs
│     ├── validated/         # Validation reports
│── scripts/                 # ETL + validation + analytics + retry logic
│── seed_data.json           # Primary Pav Bhaji seed recipe
│── serviceAccount.json       # Firestore service key (ignored in git)
│── .env                     # Secure variable storage
│── requirements.txt
│── README.md

📌 3. Data Model (ER Models)

This pipeline uses two data models:

🔷 A. Firestore ERD (Source Model — Nested NoSQL)
 ┌─────────────────────┐
 │       RECIPES       │
 │─────────────────────│
 │ id (PK)             │
 │ title               │
 │ description         │
 │ ingredients[]       │───┐
 │ steps[]             │──┐│
 │ difficulty          │  ││ Nested arrays
 │ prep_time           │  ││
 │ cook_time           │  ││
 │ tags[]              │  ││
 └────────────┬────────┘  ││
              │           ││
     ┌────────▼───────┐   ││
     │  INTERACTIONS  │   ││
     │────────────────│   ││
     │ id (PK)        │   ││
     │ recipe_id (FK) │◀──┘│
     │ user_id (FK)   │◀────┘
     │ type           │
     │ rating         │
     └────────┬───────┘
              │
    ┌─────────▼────────┐
    │       USERS       │
    └───────────────────┘

🔷 B. CSV / Analytics ERD (Flattened Model)
 RECIPES_CLEAN
      │ id (PK)
      │ title, difficulty, prep_time, …
      │
      ├───────────────┐
      ▼               ▼
INGREDIENTS_CLEAN   STEPS_CLEAN
recipe_id (FK)      recipe_id (FK)
ingredient_name     order
quantity            text

INTERACTIONS_CLEAN
recipe_id (FK)
user_id (FK)

USERS_CLEAN
id (PK)

📌 4. Firebase Source Data Setup
🔐 Secrets (Stored Securely)

The project uses:

serviceAccount.json

.env → contains SERVICE_ACCOUNT_PATH & PAV_SEED_PATH

Both ignored via .gitignore.

📌 Primary Dataset: Pav Bhaji (seed_data.json)

This is the main real recipe used to fulfill assignment requirements.

Includes:

Real ingredients

Real step-by-step instructions

Difficulty, region, cuisine metadata

📌 Synthetic Dataset Generated

The pipeline auto-generates:

19 vegetarian recipes

10 users

360+ interactions

Inserted into Firestore collections:

recipes

users

interactions

📌 5. ETL / ELT Pipeline Steps
🟦 Step 1 — Setup Firestore

scripts/1_setup_firestore.py

Inserts Pav Bhaji (primary seed dataset)

Generates vegetarian recipes

Creates users

Inserts interactions

Includes retry logic for Firestore operations

Uses .env for secure secrets

🟦 Step 2 — Export Firestore → JSON

scripts/2_export_firestore.py

Exports:

exports/recipes.json
exports/users.json
exports/interactions.json


Includes:

Retry logic

Logging

🟦 Step 3 — Transform JSON → Normalized CSV

scripts/3_transform_to_csv.py

Outputs (clean tables):

outputs/clean/recipes_clean.csv
outputs/clean/ingredients_clean.csv
outputs/clean/steps_clean.csv
outputs/clean/users_clean.csv
outputs/clean/interactions_clean.csv

🟦 Step 4 — Data Validation

Two layers:

A. Basic Validation (4_validate_csv.py)

Checks:

Required columns

No missing recipe/user IDs

Positive times

Step ordering

Duplicate detection

B. Custom Great-Expectations-Style Validation

scripts/4a_custom_expectations_check.py

Generates:

outputs/validated/custom_ge_report.txt


Checks:

Column existence

Null checks

Uniqueness

Integer-like values

Foreign key integrity

100% Python 3.14 compatible.

🟦 Step 5 — Analytics & Visualization

scripts/5_analytics.py

Generates:

Ingredient frequency chart

Difficulty distribution

Top 10 viewed recipes

Step count distribution

User activity

Prep vs likes correlation

Complexity score

Engagement score

Outputs (examples):

analysis/top_ingredients.png
analysis/difficulty_distribution.png
analysis/top_viewed_recipes.png
analysis/complexity_distribution.png
analysis/insights_summary.txt

📌 6. Key Data Quality Rules
✔ Recipes

Must contain id, title, difficulty

prep/cook times ≥ 0

difficulty ∈ {easy, medium, hard}

✔ Ingredients

recipe_id required

ingredient_name required

✔ Steps

valid integer step order

all steps must belong to a recipe

✔ Interactions

recipe_id and user_id must exist

type ∈ {view, like, cook_attempt}

rating ∈ {1–5 or NULL}

📌 7. Orchestration (Automated Pipeline)

run_pipeline.py orchestrates:

1. Setup Firestore
2. Export JSON
3. Transform CSV
4. Validate data
5. Run analytics


One command runs the entire pipeline:

python scripts/run_pipeline.py

📌 8. How to Run
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Place Firestore Key

Place your secure:

serviceAccount.json


inside project root.

3️⃣ Set environment variables

Create .env:

SERVICE_ACCOUNT_PATH=serviceAccount.json
PAV_SEED_PATH=seed_data.json

4️⃣ Run Pipeline
python scripts/run_pipeline.py

📌 9. Limitations

Synthetic recipes not real-world accurate

Ratings are randomly generated

Project assumes working Firestore configuration

Primarily vegetarian dataset

📌 10. Deliverables Included

Full ETL pipeline

JSON exports

Normalized CSV datasets

Custom data quality validation (GE-style)

Charts + insights

Complete orchestration

Full README for assignment

📘 Conclusion

This project demonstrates a fully functional Data Engineering workflow, transforming semi-structured Firestore data into validated analytical datasets. It includes:

Data modeling

Secure key handling

Firestore ingestion

ETL/ELT processing

Data validation

Analytics

Orchestration

It is structured, professional, and suitable for academic submission or real-world Data Engineering evaluation.
