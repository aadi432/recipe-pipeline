import subprocess
import sys
import os
import logging
from dotenv import load_dotenv

# =====================================================
# 1. LOGGING CONFIGURATION
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =====================================================
# 2. LOAD ENVIRONMENT VARIABLES
# =====================================================
load_dotenv()

SCRIPTS_DIR = os.getenv("SCRIPTS_DIR", "scripts")

# =====================================================
# 3. SAFE SCRIPT RUNNER
# =====================================================
def run_script(script_name):
    """Runs a python script inside the same venv."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    logger.info(f"▶ Running: {script_name}")

    try:
        result = subprocess.run([sys.executable, script_path], check=True)
        logger.info(f"✔ Completed: {script_name}")

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error in script: {script_name}")
        logger.error(e)
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Unexpected error in {script_name}: {e}")
        sys.exit(1)


# =====================================================
# 4. PIPELINE EXECUTION ORDER
# =====================================================
if __name__ == "__main__":
    logger.info("\n============= RECIPE ANALYTICS PIPELINE =============")

    run_script("1_setup_firestore.py")
    run_script("2_export_firestore.py")
    run_script("3_transform_to_csv.py")
    run_script("4_validate_csv.py")
    run_script("5_analytics.py")

    logger.info("=====================================================")
    logger.info("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    logger.info("📦 Check folders:")
    logger.info("   - exports/   (Raw Firebase JSON)")
    logger.info("   - outputs/   (CSV files)")
    logger.info("   - analysis/  (Charts + Insights)")
    logger.info("=====================================================\n")
