# scripts/run_pipeline.py
import subprocess
import sys
import os
import time

print("\n=============== RECIPE ANALYTICS PIPELINE ===============\n")

# Convert Windows path issues (safely handles spaces)
def run_script(script_name):
    script_path = os.path.join("scripts", script_name)
    print(f"\n▶ Running: {script_name}")
    try:
        result = subprocess.run([sys.executable, script_path], check=True)
        print(f"✔ Completed: {script_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Error in: {script_name}")
        sys.exit(1)


# 1. FIRESTORE SETUP

run_script(r"C:\Users\DELL\Desktop\recipe-pipeline\scripts\1_setup_firestore.py")
time.sleep(2)


# 2. EXPORT RAW JSON FROM FIRESTORE

run_script(r"C:\Users\DELL\Desktop\recipe-pipeline\scripts\2_export_firestore.py")
time.sleep(2)

# 3. TRANSFORM FIRESTORE → CSV OUTPUTS

run_script(r"C:\Users\DELL\Desktop\recipe-pipeline\scripts\3_transform_to_csv.py")
time.sleep(2)

# 4. VALIDATE CSV OUTPUTS

run_script(r"C:\Users\DELL\Desktop\recipe-pipeline\scripts\4_validate_csv.py")
time.sleep(2)


# 5. PERFORM ANALYTICS + CHARTS

run_script(r"C:\Users\DELL\Desktop\recipe-pipeline\scripts\5_analytics.py")
time.sleep(2)

print("\n============================================================")
print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
print("📦 Check folders:")
print("   - exports/  (raw Firebase dumps)")
print("   - outputs/  (normalized CSVs)")
print("   - analysis/ (charts + insights)")
print("============================================================\n")
