# recipe-pipeline

# Recipe Analytics Pipeline (Firebase + Python)

This document serves as a complete **Data Engineering assignment submission**, covering data modeling, Firebase data setup, ETL/ELT workflows, data quality validation, analytics, and automated pipeline orchestration.

The project demonstrates how semi-structured NoSQL data from Firestore can be transformed into clean, validated, analytical datasets.

---

## 📌 1. Project Overview

This assignment implements an end-to-end data pipeline that:

* Inserts seed + synthetic recipe data into Firebase Firestore
* Exports Firestore collections into JSON
* Transforms JSON into normalized CSV tables
* Validates the CSV tables using custom data-quality rules
* Generates analytical insights and visualization charts
* Runs all steps automatically through a single orchestrated pipeline script

Folder structure:

    recipe-pipeline/
    │── analysis/          # Charts + insights
    │── exports/           # Raw JSON exports from Firestore
    │── outputs/           # Normalized CSVs + validation report
    │── scripts/           # ETL, validation, analytics, orchestration scripts
    │── seed_data.json     # Primary Pav Bhaji recipe
    │── serviceAccount.json
    │── requirements.txt
    │── README.md

---

## 📌 2. Data Model (ER Diagram)

Below is the complete ER diagram using Mermaid (tildes used so code does not break):

### **Mermaid ER Diagram**

~~~mermaid
erDiagram
    USERS {
        string id
        string name
    }

    RECIPES {
        string id
        string title
        string description
        int prep_time
        int cook_time
        string difficulty
        string cuisine
        string region
        string created_at
    }

    INGREDIENTS {
        string recipe_id
        string ingredient_name
        string ingredient_quantity
    }

    STEPS {
        string recipe_id
        int step_order
        string step_text
    }

    INTERACTIONS {
        string id
        string recipe_id
        string user_id
        string type
        int rating
        string timestamp
    }

    RECIPES ||--o{ INGREDIENTS : has
    RECIPES ||--o{ STEPS : includes
    USERS ||--o{ INTERACTIONS : performs
    RECIPES ||--o{ INTERACTIONS : receives
~~~

---

## 📌 3. Firebase Source Data Setup

The Firebase setup uses a secure **Firebase Service Account key (serviceAccount.json)**.

### 🔐 Service Account / Secret Key

* Required file: serviceAccount.json  
* Used for Firestore authentication  
* Must be excluded using .gitignore  

---

## 📌 Primary Recipe (Seed Data)

Your **Pav Bhaji** recipe stored in `seed_data.json` is the **primary dataset**.

Includes:

* Ingredients  
* Steps  
* Difficulty  
* Cuisine  
* Region  
* Prep and cook time  

---

## 📌 Additional Data Setup

Created using `1_setup_firestore.py`.

### Synthetic Recipes
* 19 vegetarian recipes  

### Users
* 10 synthetic users  

### Interactions
* 120 interactions (views, likes, cook attempts)  

Firestore collections:

* recipes  
* users  
* interactions  

---

## 📌 4. ETL / ELT Pipeline Steps

### Step 1 — Firestore Setup
`scripts/1_setup_firestore.py`

### Step 2 — Export Firestore → JSON
`scripts/2_export_firestore.py`

### Step 3 — Transform JSON → CSV
`scripts/3_transform_to_csv.py`

Produces:

* recipe.csv  
* ingredients.csv  
* steps.csv  
* users.csv  
* interactions.csv  

### Step 4 — Validation
`scripts/4_validate_csv.py`  
`scripts/4a_custom_expectations_check.py`

### Step 5 — Analytics + Visualizations
`scripts/5_analytics.py`  

---

## 📌 5. Data Quality Validation Rules

### Recipes
* id, title required  
* prep_time & cook_time >= 0  
* difficulty must be easy/medium/hard  

### Ingredients
* recipe_id required  
* ingredient_name required  

### Steps
* step_order ≥ 1  
* must be sequential  

### Interactions
* type ∈ {view, like, cook_attempt}  
* rating 1–5 or null  

---

## 📌 6. Analytics & Insights

Insights generated:

* Most common ingredients  
* Most viewed recipes  
* Difficulty distribution  
* Prep time vs likes correlation  
* Step count distribution  
* User engagement ranking  
* Cuisine/region distribution  

Charts stored in `/analysis`.

---

## 📌 7. Pipeline Orchestration

All tasks automated using:

### `run_pipeline.py`

This script:

* Runs ingestion  
* Exports JSON  
* Converts data  
* Validates datasets  
* Generates charts  

---

## 📌 8. How to Run the Pipeline

Install dependencies:

    pip install -r requirements.txt

Add Firebase service key:

    serviceAccount.json (in project root)

Run full pipeline:

    python scripts/run_pipeline.py

---

## 📌 9. Limitations

* Synthetic recipes may not be accurate  
* Ratings include random values  
* Firestore must be correctly configured  
* Vegetarian-only dataset  

---

## 📌 10. Deliverables Included

* ETL scripts  
* JSON exports  
* CSV datasets  
* Validation report  
* Analytics charts  
* Orchestration script  
* This README  

---

## 📘 Conclusion

This submission demonstrates a complete academic-style **end-to-end Data Engineering pipeline**, transforming Firestore NoSQL data into clean, validated analytical datasets via structured ETL, validation, modeling, visualization, and orchestration.

---

**End of README**
