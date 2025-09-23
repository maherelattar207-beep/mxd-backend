from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import time
import random
import string

app = FastAPI()

# Temporary in-memory "database" for demo purposes
valid_purchases = {"testuser@example.com": True}  # Emails of real buyers
generated_keys = {}

class VerifyRequest(BaseModel):
    email: str

# Helper function to generate a unique license key
def generate_license_key(email: str) -> str:
    timestamp = str(int(time.time()))
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    hash_part = hashlib.sha256((email + timestamp + random_part).encode()).hexdigest()[:8].upper()
    return f"MXD-{hash_part}-{random_part}"

@app.post("/verify_purchase")
def verify_purchase(request: VerifyRequest):
    email = request.email.strip().lower()

    # 1. Check if email is a real buyer
    if email not in valid_purchases:
        raise HTTPException(status_code=403, detail="Email not verified as a buyer.")

    # 2. Generate a new license key
    new_key = generate_license_key(email)
    generated_keys[email] = new_key
    return {"status": "success", "license_key": new_key}

@app.post("/validate_key")
def validate_key(key: str):
    # Check if key exists in our generated keys
    if key in generated_keys.values():
        return {"status": "valid"}
    else:
        raise HTTPException(status_code=403, detail="Invalid or expired license key.")
