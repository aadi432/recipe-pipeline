# Recipe-Pipeline

# Recipe Analytics Pipeline (Firebase + Python)

This document serves as a complete **Data Engineering assignment submission**, covering data modeling, Firebase data setup, ETL/ELT workflows, data quality validation, analytics, and automated pipeline orchestration.

The project demonstrates how semi-structured NoSQL data from Firestore can be transformed into clean, validated, analytical datasets.

---

## 📌 1. Project Overview

This assignment implements an end‑to‑end data pipeline that:

* Inserts seed + synthetic recipe data into Firebase Firestore
* Exports Firestore collections into JSON
* Transforms JSON into normalized CSV tables
* Validates the CSV tables using custom data‑quality rules
* Generates analytical insights and visualization charts
* Runs all steps automatically through a single orchestrated pipeline script

Folder structure:

```
recipe-pipeline/
│── analysis/          # Charts + insights
│── exports/           # Raw JSON exports from Firestore
│── outputs/           # Normalized CSVs + validation report
│── scripts/           # ETL, validation, analytics, orchestration scripts
│── seed_data.json     # Primary Pav Bhaji recipe
│── serviceAccount.json
│── requirements.txt
│── README.md
```

---

## 📌 2. Data Model (ER Diagram)

### **ER Diagram Overview**

```
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
```

This model ensures:

* 1:M relationship between **recipes → ingredients**
* 1:M relationship between **recipes → steps**
* M:N relationship between **users ↔ recipes**, resolved through **interactions**

---

## 📌 3. Firebase Source Data Setup

The Firebase setup uses a **Firebase Service Account key** (`serviceAccount.json`) which acts as the secure authentication file required for connecting Python scripts to Firestore. This secret key must be placed inside the project root and **should never be shared publicly**.

### 🔐 Service Account / Secret Key

* File required: **`serviceAccount.json`**
* Used for: authenticating all Firestore operations
* Must be stored securely and excluded from public repositories via `.gitignore`

### **Primary Recipe (Seed Data)**

The project uses **Pav Bhaji** from `seed_data.json` as the **primary recipe dataset**. This is the main real recipe provided by the candidate, as required by the assignment. It includes:

* Full list of ingredients
* Step-by-step cooking procedure
* Difficulty, time, and tags

### Additional Data Setup

Source data is created using `1_setup_firestore.py`.

### **Seed Recipe (Primary Dataset)**

* Pav Bhaji (from `seed_data.json`)
* This is the **main recipe provided by the candidate**, fulfilling the requirement to use your own recipe as the primary dataset
* Contains complete ingredients and step-by-step instructions
* Pav Bhaji (from `seed_data.json`)
* Contains complete ingredients and step-by-step instructions

### **Synthetic Recipes**

* 19 additional vegetarian recipes
* Random cuisine, region, difficulty, ingredients, steps

### **Users**

* 10 sample Indian users created

### **Interactions**

* 360 synthetic interactions including:

  * `view`
  * `like`
  * `cook_attempt`
  * random optional rating values

All data is inserted into three Firestore collections:

* `recipes`
* `users`
* `interactions`

---

## 📌 4. ETL / ELT Pipeline Steps

The ETL pipeline consists of five clearly separated stages.

### **Step 1 — Firestore Setup**

`1_setup_firestore.py` inserts all seed + synthetic data.

### **Step 2 — Export Firestore → JSON**

`2_export_firestore.py` exports:

* `exports/recipes.json`
* `exports/users.json`
* `exports/interactions.json`

### **Step 3 — Transform JSON → CSV**

`3_transform_to_csv.py` normalizes Firestore data into tables:

* `recipe.csv`
* `ingredients.csv`
* `steps.csv`
* `interactions.csv`
* `users.csv`

### **Step 4 — Data Validation**

`4_validate_csv.py` enforces:

* Required fields present
* Positive prep/cook times
* Sequential step order
* Valid difficulty values
* Rating validation

Output: `outputs/validation_report.json`

### **Step 5 — Analytics + Visualizations**

`5_analytics.py` generates:

* Ingredient frequency charts
* Difficulty distribution
* Correlation analysis
* Top views + likes
* User activity rankings
* Step count analysis

Outputs stored in `analysis/`.

---

## 📌 5. Data Quality Validation Rules

Validation ensures dataset consistency.

### **Recipe Validation**

* id, title, difficulty required
* prep/cook times must be ≥ 0
* difficulty ∈ {easy, medium, hard}
* tags must not be empty

### **Ingredient Validation**

* recipe_id, ingredient_name required

### **Interaction Validation**

* id, recipe_id, user_id, type required
* type must be valid
* rating must be numeric & within [1–5]

### **Steps Validation**

* step_order must be positive
* step sequence must be correct per recipe

---

## 📌 6. Analytics & Insights Generated

The analytics module produces at least 10 insights:

1. Most common ingredients
2. Average preparation time
3. Average total cooking time
4. Difficulty distribution
5. Prep-time vs likes correlation
6. Most viewed recipes
7. Ingredient frequency in high-engagement recipes
8. Step count distribution
9. Most active users
10. Full insights summary text file

Charts and summary files appear in the **analysis** folder.

---

## 📌 7. Pipeline Orchestration

To simulate a real data engineering workflow, all five stages are orchestrated using:

### **`run_pipeline.py`**

This script:

* Executes all pipeline steps in correct order
* Handles errors at script boundaries
* Automates data ingestion → transformation → validation → analytics
* Ensures reproducibility and consistent results

Running one command completes the entire pipeline.

---

## 📌 8. How to Run the Pipeline

### **Install Dependencies**

```
pip install -r requirements.txt
```

### **Place Firebase Service Key**

Ensure `serviceAccount.json` exists in project root.

### **Run the Full Pipeline**

```
python scripts/run_pipeline.py
```

This will:

* Load & seed data into Firestore
* Export Firestore state into JSON
* Transform JSON into normalized CSVs
* Validate the CSVs
* Generate charts + insights

---

## 📌 9. Limitations

* Synthetic recipes are randomly generated (not real-world accurate)
* Ratings are partially random
* Pipeline assumes correct Firestore configuration
* Current dataset focuses only on vegetarian recipes

---

## 📌 10. Deliverables Included

* Complete ETL + validation scripts
* JSON exports
* Normalized CSV datasets
* Validation report
* Analytics charts
* Fully orchestrated pipeline runner
* This README documentation

---

## 📘 Conclusion

This submission presents a structured, academic-style **end-to-end data engineering pipeline**. It demonstrates the transformation of NoSQL Firestore data into validated analytical datasets, supported by orchestration, modeling, validation, and visualization components.


