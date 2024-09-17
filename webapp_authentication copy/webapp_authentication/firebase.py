import firebase_admin
from firebase_admin import credentials
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# # Path to your Firebase Admin SDK key
firebase_cred_path = BASE_DIR / 'config' / 'levitate-hyperloop-webapp-firebase-adminsdk-ow8im-9c9e5d9b54.json'
print(firebase_cred_path)
 # Ensure the file exists
if not firebase_cred_path.exists():
    raise FileNotFoundError(f"Firebase credentials file not found at {firebase_cred_path}")
cred = credentials.Certificate(firebase_cred_path)
# firebase_admin.initialize_app(cred)