# 🍽️ Recipe Analytics Pipeline  
### *Firebase → Python ETL → Data Validation → Analytics → Visualizations*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?logo=firebase)
![ETL](https://img.shields.io/badge/ETL-Pipeline-green)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

---

## 📌 1. Introduction

The **Recipe Analytics Pipeline** is an end-to-end **data engineering project** that ingests nested recipe data from **Firebase Firestore**, exports it as JSON, transforms it into clean relational CSVs, validates data quality, and generates analytical visualizations.

It demonstrates:

- NoSQL → Relational data modeling  
- ETL / ELT pipeline design in Python  
- Custom data validation (Great-Expectations-style checks)  
- Orchestrated pipeline execution with logging & retry  
- Insightful analytics and charts for recipe interactions  

The primary dataset is a **real Pav Bhaji recipe**, enriched with synthetic vegetarian recipes, users, and interactions.

---

## 📁 2. Folder Structure

~~~plaintext
recipe-pipeline/
│── analysis/                # Generated charts & insights
│── exports/                 # Raw JSON exports from Firestore
│── outputs/
│     ├── clean/             # Normalized cleaned CSVs
│     └── validated/         # Validation reports
│── scripts/                 # ETL, validation, analytics, orchestration scripts
│── seed_data.json           # Primary Pav Bhaji recipe (real)
│── serviceAccount.json      # Firebase authentication key (gitignored)
│── .env                     # Secret environment variables
│── requirements.txt
│── README.md
~~~

---

## 🧠 3. System Overview

This pipeline executes a complete data workflow:

1. Insert **Pav Bhaji + synthetic recipes** into Firestore  
2. Export Firestore collections to **JSON**  
3. Transform nested JSON into **normalized CSVs**  
4. Apply **custom data validation rules**  
5. Run **analytics** and generate **11+ charts**  
6. Orchestrate all steps with a single script: `run_pipeline.py`  

---

## 🧩 4. Data Model (ER Diagrams)

### 🔷 4.1 Firestore ERD (Nested NoSQL Model)

~~~mermaid
erDiagram
    RECIPES {
        string id
        string title
        string description
        int prep_time_minutes
        int cook_time_minutes
        string difficulty
        string cuisine
        string region
        datetime created_at
    }

    INGREDIENTS {
        string recipe_id
        string name
        string quantity
    }

    STEPS {
        string recipe_id
        int order
        string text
    }

    INTERACTIONS {
        string id
        string recipe_id
        string user_id
        string type
        int rating
        datetime timestamp
    }

    USERS {
        string id
        string name
    }

    RECIPES ||--o{ INGREDIENTS : "contains"
    RECIPES ||--o{ STEPS : "has"
    RECIPES ||--o{ INTERACTIONS : "receives"
    USERS ||--o{ INTERACTIONS : "performs"
~~~

---

### 🔷 4.2 CSV / Analytics ERD (Flattened Relational Model)

~~~mermaid
erDiagram
    RECIPES_CLEAN {
        string id
        string title
        int prep_time_minutes
        int cook_time_minutes
        int total_time
        string difficulty
        float complexity_score
        float engagement_score
    }

    INGREDIENTS_CLEAN {
        string recipe_id
        string ingredient_name
        string quantity
    }

    STEPS_CLEAN {
        string recipe_id
        int order
        string step_text
    }

    USERS_CLEAN {
        string id
        string name
    }

    INTERACTIONS_CLEAN {
        string id
        string recipe_id
        string user_id
        string type
        int rating
        datetime timestamp
    }

    RECIPES_CLEAN ||--o{ INGREDIENTS_CLEAN : contains
    RECIPES_CLEAN ||--o{ STEPS_CLEAN : includes
    RECIPES_CLEAN ||--o{ INTERACTIONS_CLEAN : receives
    USERS_CLEAN ||--o{ INTERACTIONS_CLEAN : performs
~~~

---

## 🍛 5. Primary Dataset

### 🟢 Pav Bhaji (Primary Real Recipe)

- Provided by the candidate  
- Contains full ingredients, steps, and metadata  
- Acts as the **primary seed recipe** in Firestore  

### 🟡 Synthetic Data

- 19 additional vegetarian recipes  
- 10 users  
- 120+ user interactions (views, likes, cook attempts)  

---

## ⚙️ 6. ETL / ELT Pipeline Steps

### Step 1 — Insert Data into Firestore  
**Script:** `scripts/1_setup_firestore.py`  

- Loads `seed_data.json` (Pav Bhaji)  
- Generates synthetic recipes, users, and interactions  
- Inserts all documents into Firestore collections  

---

### Step 2 — Export Firestore → JSON  
**Script:** `scripts/2_export_firestore.py`  

- Reads from Firestore collections  
- Exports data to JSON in the `exports/` folder  
- Creates a semi-structured snapshot of the database  

---

### Step 3 — Transform JSON → Clean CSV  
**Script:** `scripts/3_transform_to_csv.py`  

- Flattens nested recipe, ingredient, step, user, and interaction structures  
- Generates relational-style CSVs into `outputs/clean/`  
- Adds derived fields (e.g., `total_time`, `complexity_score`, `engagement_score`)  

---

### Step 4 — Validate CSVs  
**Scripts:**  
- `scripts/4_validate_csv.py`  
- `scripts/4a_custom_expectations_check.py`  

Key checks:

- Schema validation  
- Null checks on critical fields  
- Value range checks (e.g., rating 1–5)  
- Categorical checks on difficulty and interaction type  

Validation results are stored in `outputs/validated/`.

---

### Step 5 — Analytics & Visualizations  
**Script:** `scripts/5_analytics.py`  

Generates:

- Ingredient frequency charts  
- Difficulty distribution  
- Top viewed recipes  
- Prep time vs likes analysis  
- Step count distributions  
- Engagement score rankings  

Charts are saved into `analysis/`.

---

### Step 6 — Pipeline Orchestration  
**Script:** `scripts/run_pipeline.py`  

- Runs **all steps** in the correct sequence  
- Includes basic **logging** and **retry logic** for robustness  
- Acts as a single entry point for the entire pipeline  

---

## 🧪 7. Data Quality Rules Summary

### 🟦 Recipes

- `id`, `title` are required  
- `difficulty` ∈ {`easy`, `medium`, `hard`}  
- `prep_time_minutes` ≥ 0  
- `cook_time_minutes` ≥ 0  

### 🟩 Ingredients

- `recipe_id` is required  
- `ingredient_name` must not be null  

### 🟨 Steps

- `order` ≥ 1  
- Steps are ordered sequentially per recipe  

### 🟧 Users

- `id` is unique  
- `name` is not null  

### 🟥 Interactions

- `type` ∈ {`view`, `like`, `cook_attempt`}  
- `rating` ∈ {1, 2, 3, 4, 5} or null  

---

## 📊 8. Sample Insights Generated

The analytics step produces insights such as:

- Most frequent ingredients across recipes  
- Distribution of recipe difficulty (easy/medium/hard)  
- Relationship between **prep time** and **number of likes**  
- Top 10 most viewed recipes  
- Average number of steps per recipe  
- Engagement score ranking for recipes  
- User interaction patterns (views vs likes vs cook attempts)  

These insights are supported by multiple charts saved in the `analysis/` directory.

---

## ▶️ 9. How to Run the Pipeline

### 9.1 Install Dependencies

~~~bash
pip install -r requirements.txt
~~~

---

### 9.2 Configure Environment Variables

Create a `.env` file in the project root:

~~~bash
SERVICE_ACCOUNT_PATH=serviceAccount.json
PAV_SEED_PATH=seed_data.json
~~~

- `serviceAccount.json`: Firebase service account key (keep secret)  
- `seed_data.json`: Contains the primary Pav Bhaji recipe and base data  

---

### 9.3 Run the Pipeline

~~~bash
python scripts/run_pipeline.py
~~~

This will:

1. Setup Firestore  
2. Export data to JSON  
3. Transform JSON to CSV  
4. Validate CSVs  
5. Run analytics and generate charts  

---

## 🚧 10. Limitations

- Ratings for synthetic interactions are partially random  
- Pipeline currently focuses **only on vegetarian recipes**  
- Requires a correctly configured Firebase Firestore project and service account  
- Validation is implemented via custom logic, not the full Great Expectations framework  

---

## 🎯 11. Conclusion

The **Recipe Analytics Pipeline** successfully demonstrates how to build a **production-style data engineering solution** on top of Firebase Firestore.  
It covers the entire lifecycle from:

- Data ingestion (NoSQL)  
- Semi-structured export (JSON)  
- Structured transformation (CSV)  
- Data quality enforcement  
- Analytical modeling  
- Visualization and insights  

By combining a **real Pav Bhaji recipe** with synthetic data, the project simulates realistic analytical workloads while still being lightweight and reproducible. The modular script-based design makes it easy to extend, maintain, and integrate into more advanced orchestration or reporting systems.

---

## 🚀 12. Future Scope

Potential enhancements include:

- Integrating **Apache Airflow** or **Prefect** for advanced workflow orchestration  
- Building an interactive **Streamlit** or **Dash** application on top of the analytics layer  
- Adding **recommendation systems** (similar recipes based on ingredients, cuisine, time)  
- Implementing **anomaly detection** for data quality and unusual user behavior  
- Extending data to include non-vegetarian and international cuisines  
- Deploying the pipeline on cloud platforms (GCP/AWS) with scheduled runs  
- Adding **CI/CD integration** to run validations automatically on new data  

---

## 📚 13. References

- Firebase Firestore Documentation  
- Python `pandas` Official Documentation  
- Concepts inspired by **Great Expectations** data validation framework  
- `matplotlib` and `seaborn` documentation for visualizations  
- Google Cloud Service Account & Authentication Guides  

---

## 👨‍💻 14. Author

**Aditya Shukla**  
Data Engineering & Analytics Pipeline Developer  
