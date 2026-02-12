from flask import Flask, jsonify, Response, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

# ===== CREDITS =====
DEVELOPER = "AKASH HACKER"

# ===== KEYS DATABASE =====
KEYS_DB = {
    "user1": {"key": "AKASH_PAID31DAYS", "expiry": "2026-03-31"}, 
    "user2": {"key": "AKASH_PAID1DAYS", "expiry": "2026-02-12"},
    "trial": {"key": "AKASH_PAID3MONTH", "expiry": "2026-04-29"},
}

@app.route('/')
def home():
    return jsonify({"message": "AKASH HACKER API is Running!", "dev": DEVELOPER})

@app.route('/akash/info/<uid>')
def get_ff_data(uid):
    user_key = request.args.get('key')

    # 1. Key Check
    if not user_key:
        return jsonify({"success": False, "error": "API Key missing!"}), 401

    found_user = next((u for u in KEYS_DB.values() if u['key'] == user_key), None)

    if not found_user:
        return jsonify({"success": False, "error": "Invalid API Key!"}), 401

    # 2. Expiry Check
    today = datetime.now()
    expiry_date = datetime.strptime(found_user['expiry'], "%Y-%m-%d")

    if today > expiry_date:
        return jsonify({"success": False, "error": "Key Expired!"}), 403

    days_left = (expiry_date - today).days

    try:
        # 3. External API Call
        api_url = f"https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO"
        response = requests.get(api_url, timeout=15)
        raw_data = response.json()

        if not raw_data or "basicInfo" not in raw_data:
            return jsonify({"success": False, "message": "UID Not Found"})

        # 4. Same to Same Response + Your Branding
        # Note: captainBasicInfo me wahi data dala hai jo basicInfo me hai (duplicate fix)
        final_data = {
            "success": True,
            "developer": DEVELOPER,
            "key_details": {
                "status": "Active",
                "expiry_date": found_user['expiry'],
                "days_remaining": f"{days_left} Days" if days_left > 0 else "Last Day Today"
            },
            "basicInfo": raw_data.get("basicInfo"),
            "captainBasicInfo": raw_data.get("basicInfo"), # Yeh raha woh fix!
            "clanBasicInfo": raw_data.get("clanBasicInfo"),
            "creditScoreInfo": raw_data.get("creditScoreInfo"),
            "diamondCostRes": raw_data.get("diamondCostRes"),
            "petInfo": raw_data.get("petInfo"),
            "profileInfo": raw_data.get("profileInfo"),
            "socialInfo": raw_data.get("socialInfo"),
            "owner_contact": "https://t.me/AkashExploits1"
        }

        # JSON Formatting (Indent 2 taaki sundar dikhe)
        json_output = json.dumps(final_data, ensure_ascii=False, indent=2)
        return Response(json_output, content_type="application/json; charset=utf-8")

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

exposed_app = app 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
