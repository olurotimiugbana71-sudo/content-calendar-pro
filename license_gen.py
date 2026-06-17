import hashlib, uuid, json, os
from datetime import datetime, timedelta

class LicenseManager:
    def __init__(self):
        self.secret_key = "CAL2026-PRO"
        self.license_file = "licenses.json"
        self.licenses = {}
        if os.path.exists(self.license_file):
            with open(self.license_file) as f:
                self.licenses = json.load(f)
    
    def save(self):
        with open(self.license_file, 'w') as f:
            json.dump(self.licenses, f, indent=2)
    
    def generate_key(self, email, tier="standard", days=30):
        uid = str(uuid.uuid4())[:8]
        raw = f"{email}{uid}{self.secret_key}{tier}{days}"
        key = hashlib.sha256(raw.encode()).hexdigest()[:20].upper()
        formatted = f"CAL-{key[:4]}-{key[4:8]}-{key[8:12]}"
        self.licenses[formatted] = {
            "email": email, "tier": tier,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=days)).isoformat()
        }
        self.save()
        return formatted
    
    def validate(self, key, email=""):
        if key in self.licenses:
            data = self.licenses[key]
            if datetime.now() > datetime.fromisoformat(data["expires"]):
                return False, "Expired"
            if email and data["email"].lower() != email.lower():
                return False, "Email mismatch"
            days_left = (datetime.fromisoformat(data["expires"]) - datetime.now()).days
            return True, f"Valid - {days_left} days left"
        return False, "Invalid"

if __name__ == "__main__":
    lm = LicenseManager()
    email = input("Buyer email: ")
    tier = input("Tier (basic/standard/premium): ")
    days = int(input("Days (30): ") or "30")
    key = lm.generate_key(email, tier, days)
    print(f"\nLICENSE: {key}")