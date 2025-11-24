
Recipe Analytics Pipeline (Firebase + Python)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?logo=firebase)
![ETL](https://img.shields.io/badge/Pipeline-ETL-green)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

---

This document serves as a complete Data Engineering assignment submission, covering data modeling, Firebase data setup, ETL/ELT workflows, custom data quality validation (GE-style), analytics, logging, retry logic, and automated pipeline orchestration.

The project demonstrates how semi-structured NoSQL data from Firestore can be transformed into clean, validated, analytical datasets with end-to-end automation.

📌 1. Project Overview

This assignment implements an end-to-end data pipeline that:

Inserts seed + synthetic recipe data into Firebase Firestore

Uses retry logic and logging for stable Firestore operations

Exports Firestore collections into JSON

Transforms nested JSON into normalized CSV tables

Validates the CSV tables using:

Basic validation rules

Custom Great Expectations–style checks (Python 3.14 compatible)

Generates analytical insights and charts

Runs all steps automatically through a single orchestrated pipeline script

Folder structure:
recipe-pipeline/
│── analysis/                   # Charts + insights
│── exports/                    # Raw JSON exports from Firestore
│── outputs/                    # Normalized CSVs + validation reports
│── scripts/                    # ETL, validation, analytics, orchestration scripts
│── seed_data.json              # Primary Pav Bhaji recipe (real data)
│── serviceAccount.json         # Firebase secret key (gitignored)
│── .env                        # SECRET + PATH variables
│── requirements.txt
│── README.md

📌 2. Data Model (ER Diagram)
ER Diagram Overview
   ┌──────────────────┐        ┌──────────────────┐
   │     USERS        │        │     RECIPES      │
   │──────────────────│        │──────────────────│
   │ id (PK)          │        │ id (PK)          │
   │ name             │        │ title            │
   └────────┬─────────┘        │ description      │
            │                  │ servings         │
            │                  │ prep_time        │
            │                  │ cook_time        │
            │                  │ difficulty       │
            │                  │ cuisine          │
            │                  │ region           │
            │                  │ created_at       │
            │                  └────────┬─────────┘
            │                           │
   ┌────────▼────────┐      ┌───────────▼──────────┐
   │  INTERACTIONS   │      │     INGREDIENTS      │
   │─────────────────│      │──────────────────────│
   │ id (PK)         │      │ recipe_id (FK)       │
   │ recipe_id (FK)  │      │ ingredient_name      │
   │ user_id (FK)    │      │ ingredient_quantity  │
   │ type            │      └──────────────────────┘
   │ rating          │
   │ timestamp       │
   └────────┬────────┘
            │
   ┌────────▼─────────┐
   │       STEPS       │
   │───────────────────│
   │ recipe_id (FK)    │
   │ step_order        │
   │ step_text         │
   └───────────────────┘


This model ensures:

1:M relationship between recipes → ingredients

1:M relationship between recipes → steps

M:N relationship between users ↔ recipes, resolved through interactions

📌 3. Firebase Source Data Setup

The Firebase setup uses a Firebase Service Account key (serviceAccount.json) which acts as the secure authentication file required for connecting Python scripts to Firestore.

This secret key is loaded through:

SERVICE_ACCOUNT_PATH in .env


and is gitignored for security.

🔐 Service Account / Secret Key

File required: serviceAccount.json

Used for: authenticating all Firestore operations

Stored securely and ignored via .gitignore

Primary Recipe (Seed Data)

The project uses Pav Bhaji from seed_data.json as the primary dataset.
It includes:

Full ingredients

Step-by-step instructions

Tags, difficulty, cuisine

Created_at timestamp

This fulfills the assignment requirement of providing your own recipe dataset.

Additional Data Setup

Data creation is handled by 1_setup_firestore.py, which now includes:

✔ Retry Logic

Stable Firestore connections & writes using exponential backoff.

✔ Logging

Every step prints meaningful INFO/WARNING/ERROR logs.

Synthetic Recipes

19 additional vegetarian recipes

Random ingredients + steps

Random difficulty, cuisine, region

Created with helper functions

Users

10 sample Indian users

Interactions

120+ interactions:

views

likes

cook_attempt

optional ratings

Data inserted into Firestore collections:

recipes

users

interactions

📌 4. ETL / ELT Pipeline Steps
Step 1 — Firestore Setup

1_setup_firestore.py inserts seed + synthetic data using:

✔ Retry logic
✔ Logging
✔ Secrets from .env

Step 2 — Export Firestore → JSON

2_export_firestore.py exports:

exports/recipes.json

exports/users.json

exports/interactions.json

Uses retry logic for Firestore read instability.

Step 3 — Transform JSON → CSV

3_transform_to_csv.py normalizes Firestore data into:

recipe.csv

ingredients.csv

steps.csv

interactions.csv

users.csv

With:

✔ Retry logic for reading CSV
✔ Fully flattened ingredients & steps
✔ Cleaned & standardized fields

📌 5. Data Validation

Validation done in two layers:

A. Basic Validation (4_validate_csv.py)

Enforces:

Required fields

Valid difficulty values

Positive times

Sequential steps

Correct rating values

Clean recipe_id & user_id mapping

B. Custom GE-Style Validation (4a_custom_expectations_check.py)

Because Great Expectations is incompatible with Python 3.14,
we implemented a custom GE-like engine with:

expect_column_to_exist

expect_values_not_null

expect_values_unique

expect_valid_difficulty

foreign key checks

integer type checks

Output file:

outputs/validated/custom_ge_report.txt

📌 6. Analytics & Insights Generated

5_analytics.py generates:

Most common ingredients

Average preparation time

Average total time

Difficulty distribution

Prep-time vs likes correlation

Most viewed recipes

High-engagement ingredients

Step count distribution

Most active users

Engagement score analysis

Complexity score distribution

Complete summary report

Charts & text files appear in:

analysis/

📌 7. Pipeline Orchestration

Using run_pipeline.py, the entire pipeline runs in order:

Setup Firestore

Export

Transform

Validate

Analytics

Includes:

✔ Logging
✔ Error handling
✔ Retry logic on critical steps

Run using:

python scripts/run_pipeline.py

📌 8. How to Run the Pipeline
Install Dependencies
pip install -r requirements.txt

Place Firebase Service Key

Ensure:

serviceAccount.json


exists in project root.

Run Pipeline
python scripts/run_pipeline.py

📌 9. Limitations

Synthetic recipes are randomly generated

Ratings partially random

Requires properly configured Firestore

Dataset currently vegetarian-focused

📌 10. Deliverables Included

✔ ETL + transformation scripts
✔ JSON exports
✔ Clean CSV datasets
✔ Basic validation + custom GE-style validation
✔ Analytics charts
✔ Summary reports
✔ Full orchestration script
✔ Complete README.md

📘 Conclusion

This submission presents a complete end-to-end Data Engineering pipeline that reflects modern, production-style practices.
From Firestore NoSQL ingestion to CSV transformation, validation, retry logic, analytics, and pipeline orchestration—every stage demonstrates a strong understanding of real-world Data Engineering workflows.

The project transforms complex Firestore documents into clean, validated analytical datasets, ensuring accuracy, reliability, and repeatability. It stands as a professional-quality assignment suitable for academic submission, interviews, and portfolio presentation.
