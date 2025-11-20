# recipe-pipeline
# Recipe Analytics Pipeline (Firebase + Python)

## 1. Project Overview
This project implements a complete end-to-end data engineering pipeline using Firebase Firestore as the source system. The pipeline covers:

- Data Modeling  
- Firestore Data Population (Real + Synthetic)  
- ETL (Extract → Transform → Load)  
- Data Validation  
- Analytics + Visualization  
- Documentation  

The purpose of this project is to demonstrate the ability to design, build, validate, and analyze a modern data pipeline using cloud infrastructure and Python.

---

## 2. Data Model

### 2.1 Recipes Collection
Stores structured recipe metadata.

| Field             | Type          | Description                |
|-------------------|---------------|----------------------------|
| id                | string        | Unique recipe ID           |
| title             | string        | Name of recipe             |
| description       | string        | Short description          |
| servings          | number        | Servings count             |
| prep_time_minutes | number        | Preparation time           |
| cook_time_minutes | number        | Cooking time               |
| difficulty        | string        | easy / medium / hard       |
| tags              | array         | Category tags              |
| ingredients       | array(map)    | Ingredient name + quantity |
| steps             | array(map)    | Ordered steps              |
| created_at        | string        | Timestamp                  |

### 2.2 Ingredients Table (Derived)
| Field               | Type   |
|---------------------|--------|
| recipe_id           | string |
| ingredient_name     | string |
| ingredient_quantity | string |

### 2.3 Steps Table (Derived)
| Field      | Type   |
|------------|--------|
| recipe_id  | string |
| step_order | number |
| step_text  | string |

### 2.4 Users Collection
| Field | Type   |
|-------|--------|
| id    | string |
| name  | string |

### 2.5 Interactions Collection
| Field     | Type                              |
|-----------|-----------------------------------|
| id        | string                            |
| recipe_id | string                            |
| user_id   | string                            |
| type      | string (view, like, cook_attempt) |
| timestamp | string                            |
| rating    | number (optional)                 |   

---

## 3. Firebase Source Data Setup

### 3.1 Service Account Setup
- Generated admin key from Firebase console  
- Saved as: `serviceAccount.json` in the project root

### 3.2 Seed Data
- Created my own recipe (Pav Bhaji) in `seed_data/pav_bhaji.json`

### 3.3 Synthetic Data
- 16 realistic synthetic recipes  
- 120 user interactions  
- 10 users with real names  

Script used:
```
scripts/1_setup_firestore.py
```

---

## 4. ETL Process

### Extract
Data pulled from Firebase using Firebase Admin SDK.

### Transform
Data normalized into:
- recipe.csv  
- ingredients.csv  
- steps.csv  
- interactions.csv  
- users.csv  

Script:
```
scripts/3_transform_to_csv.py
```

### Load
All CSVs stored inside `/outputs`.

---

## 5. Data Validation

Validation rules implemented:

### ✔ Required fields  
### ✔ Numeric ranges  
### ✔ Difficulty category check  
### ✔ Interaction type check  
### ✔ Rating range (1–5)  
### ✔ Step-order correctness  
### ✔ Missing values  

Script:
```
scripts/4_validate_csv.py
```

Output:
```
outputs/validation_report.json
```

---

## 6. Analytics & Insights

Script:
```
scripts/5_analytics.py
```

Outputs stored inside `/charts`.

### Key Insights Generated:
1. **Most common ingredients**
2. **Average prep time & total time**
3. **Difficulty distribution**
4. **Correlation between prep time and likes**
5. **Top viewed recipes**
6. **High-engagement ingredients**
7. **Step count analysis**
8. **Most active users**

Summary file:
```
charts/insights_summary.txt
```

Charts include:
- top_ingredients.png  
- difficulty_distribution.png  
- top_viewed_recipes.png  
- avg_prep_total_time.png  
- high_engagement_ingredients.png  
- top_step_counts.png  
- top_active_users.png  

---

## 7. How to Run the Pipeline

### 7.1 Install Requirements
```
python -m venv venv
venv/Scripts/activate       # Windows
pip install -r requirements.txt
```

### 7.2 Run All Steps

**STEP 1 — Populate Firestore**
```
python scripts/1_setup_firestore.py
```

**STEP 2 — ETL**
```
python scripts/3_transform_to_csv.py
```

**STEP 3 — Validation**
```
python scripts/4_validate_csv.py
```

**STEP 4 — Analytics**
```
python scripts/5_analytics.py
```

---

## 8. Deliverables

- ✔ ETL scripts  
- ✔ Validation script  
- ✔ Normalized CSV output  
- ✔ Analytics summary document  
- ✔ Visualization charts  
- ✔ README.md  

---

## 9. Known Limitations
- Synthetic data is randomly generated  
- Timestamps stored as strings  
- No incremental (delta) ETL  
- Limited user behavioral depth  
- Firestore used in simple form (no subcollections)

---

## 10. Conclusion
This project demonstrates a complete data engineering workflow using Firebase and Python, including modeling, ETL, validation, analytics, and reporting.  
It satisfies all requirements in the assessment and provides clean, structured, and insightful output.
