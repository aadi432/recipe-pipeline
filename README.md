🧑‍🍳 Recipe Analytics Pipeline (Firebase + Python)










A complete end-to-end Data Engineering Pipeline that ingests recipe data from Firebase Firestore, transforms it into analytical tables, validates the data using a custom Great-Expectations-style framework, and generates insights and visualizations — all automated through a Python orchestration script.

Designed as a production-ready Data Engineering assignment and a portfolio-quality project.

📌 Table of Contents

Project Overview

Folder Structure

Data Model (ER Diagrams)

Firestore Setup

ETL / ELT Pipeline

Data Quality Validation

Analytics & Visualizations

Pipeline Orchestration

How to Run

Limitations

Conclusion

🚀 Project Overview

This project demonstrates a realistic Data Engineering workflow by transforming semi-structured Firestore data into clean, validated, and analytics-ready datasets.

✔ Firestore ingestion (seed + synthetic data)
✔ Export collections to JSON
✔ Transform JSON → CSV
✔ Validate using custom expectations
✔ Generate insights & charts
✔ One-click pipeline automation

The primary dataset is a real recipe:
🥘 Pav Bhaji (from seed_data.json)
This fulfills the assignment requirement to include your own recipe.

📁 Folder Structure
recipe-pipeline/
│── analysis/                # Charts + insight summaries
│── exports/                 # Raw Firestore exports
│── outputs/
│     ├── clean/             # Normalized CSVs
│     ├── validated/         # Validation reports
│── scripts/                 # All ETL + validation + analytics scripts
│── seed_data.json           # Pav Bhaji (primary dataset)
│── serviceAccount.json      # Firestore auth key (ignored in git)
│── .env                     # Contains FIREBASE paths
│── requirements.txt
│── README.md

🗂️ Data Model (ER Diagrams)
🔷 A. Firestore NoSQL Model (Nested)
 RECIPES
   ├── ingredients[]  
   ├── steps[]
   ├── metadata
   └── tags[]

 INTERACTIONS
   ├── user_id → USERS.id
   ├── recipe_id → RECIPES.id
   └── type (view/like/cook_attempt)

 USERS
   └── id, name

🔷 B. Normalized CSV ERD
RECIPES_CLEAN (PK: id)
INGREDIENTS_CLEAN (FK: recipe_id)
STEPS_CLEAN (FK: recipe_id)
INTERACTIONS_CLEAN (FK: recipe_id, user_id)
USERS_CLEAN (PK: id)

🔥 Firestore Setup
✔ Secure secret handling

serviceAccount.json stored in project root

.env stores secure paths

Both are ignored by .gitignore

✔ Primary dataset

Pav Bhaji (your real recipe)

✔ Synthetic data generated

19 vegetarian recipes

10 users

360 interactions (view/like/cook_attempt)

✔ Retry logic added

All Firestore operations use automatic retry in case of temporary failures.

🔄 ETL / ELT Pipeline
Step 1 → Ingest data into Firestore

scripts/1_setup_firestore.py

Inserts Pav Bhaji

Generates synthetic recipes

Creates users

Adds interactions

With retry logic + logging

Step 2 → Export Firestore → JSON

scripts/2_export_firestore.py
Exports:

recipes.json

users.json

interactions.json

Step 3 → Transform JSON → CSV

scripts/3_transform_to_csv.py
Outputs:

recipes_clean.csv

ingredients_clean.csv

steps_clean.csv

users_clean.csv

interactions_clean.csv

Step 4 → Data Quality Validation
A. Basic Validation

scripts/4_validate_csv.py
Ensures:

Required fields

Valid difficulty

Step order

Positive times

B. Great-Expectations-style Validation

scripts/4a_custom_expectations_check.py
Generates:

outputs/validated/custom_ge_report.txt


Validates:

Column existence

Null checks

Unique IDs

Allowed values

Foreign key checks

Fully Python 3.14 compatible.

📊 Analytics & Visualizations

scripts/5_analytics.py produces:

📌 Key charts

Top ingredients

Difficulty distribution

Prep time vs likes correlation

Top viewed recipes

Top active users

Step count distribution

Complexity score histogram

Engagement score rankings

📌 Summary insights

Saved as:

analysis/insights_summary.txt

🧩 Pipeline Orchestration

Automated through:

scripts/run_pipeline.py


Runs all stages sequentially:

Firestore setup

Export JSON

Transform to CSV

Validate data

Generate analytics

One command controls the entire workflow.

🛠️ How to Run
1. Install dependencies
pip install -r requirements.txt

2. Add secrets

Place:

serviceAccount.json


in project root.

3. Configure .env
SERVICE_ACCOUNT_PATH=serviceAccount.json
PAV_SEED_PATH=seed_data.json

4. Run complete pipeline
python scripts/run_pipeline.py

⚠️ Limitations

Synthetic recipes are randomly generated

Ratings partially randomized

Assumes valid Firebase credentials

Dataset currently vegetarian-focused

🏁 Conclusion

This project demonstrates a complete academic + production-style Data Engineering pipeline, covering:

✔ NoSQL → Structured ETL
✔ Retry logic
✔ Secure secret handling
✔ Validation
✔ Analytics
✔ Full automation
✔ ER modeling
✔ Real + synthetic datasets
