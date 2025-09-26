import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

class DatabaseManager:
    def __init__(self):
        self.client = supabase

    # ---- Users ----
    def create_user(self, name, email, password, role):
        return self.client.table("users").insert({
            "name": name,
            "email": email,
            "password": password,
            "role": role,
        }).execute()

    def get_all_users(self):
        return self.client.table("users").select("*").execute()

    def update_user(self, user_id, name=None, email=None, password=None, role=None):
        update_data = {}
        if name: update_data["name"] = name
        if email: update_data["email"] = email
        if password: update_data["password"] = password
        if role: update_data["role"] = role
        return self.client.table("users").update(update_data).eq("user_id", user_id).execute()

    def delete_user(self, user_id):
        return self.client.table("users").delete().eq("user_id", user_id).execute()

    # ---- Donations ----
    def create_donation(self, user_id, food_item, quantity, expiry_date):
        return self.client.table("donations").insert({
            "user_id": user_id,
            "food_item": food_item,
            "quantity": quantity,
            "expiry_date": expiry_date
        }).execute()

    def get_available_donations(self):
        return self.client.table("donations").select("*").eq("status", "available").execute()

    def update_donation_status(self, donation_id, status):
        return self.client.table("donations").update({"status": status}).eq("donation_id", donation_id).execute()

    def delete_donation(self, donation_id):
        return self.client.table("donations").delete().eq("donation_id", donation_id).execute()

    # ---- Requests ----
    def create_request(self, ngo_id, donation_id):
        return self.client.table("requests").insert({
            "ngo_id": ngo_id,
            "donation_id": donation_id,
            "status": "pending"
        }).execute()

    def get_requests_by_ngo(self, ngo_id):
        return self.client.table("requests").select("*").eq("ngo_id", ngo_id).execute()

    def get_requests_with_donation_info_by_ngo(self, ngo_id):
        return self.client.table("requests") \
            .select("request_id, status, donation_id, donations(food_item, expiry_date)") \
            .eq("ngo_id", ngo_id).execute()

    def update_request_status(self, request_id, status):
        return self.client.table("requests").update({"status": status}).eq("request_id", request_id).execute()

    def delete_request(self, request_id):
        return self.client.table("requests").delete().eq("request_id", request_id).execute()

    def get_request_status_by_donation(self, donation_id):
        return self.client.table("requests").select("request_id, ngo_id, status").eq("donation_id", donation_id).execute()

    def get_all_requests_with_user_info(self):
        return self.client.table("requests") \
            .select("request_id, status, donation_id, ngo:users(name), donations(food_item)") \
            .execute()
