# delete_firestore_database.py
import firebase_admin
from firebase_admin import credentials, firestore

# -------- CONFIG --------
SERVICE_ACCOUNT_PATH = r"C:\Users\DELL\Desktop\recipe-pipeline\serviceAccount.json"
# ------------------------

def delete_collection(coll_ref, batch_size=50):
    """
    Recursively delete documents in a Firestore collection.
    Deletes in batches to avoid timeouts.
    """
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f"Deleting doc: {doc.id} from {coll_ref.id}")
        
        # If subcollections exist, delete them recursively
        subcollections = doc.reference.collections()
        for sub in subcollections:
            delete_collection(sub)

        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


def delete_entire_database():
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    print("\n⚠️ WARNING: You are about to delete the entire Firestore database.\n")

    collections = db.collections()
    for coll in collections:
        print(f"\nDeleting collection: {coll.id}")
        delete_collection(coll)

    print("\n✅ All Firestore data deleted successfully!\n")


if __name__ == "__main__":
    delete_entire_database()
