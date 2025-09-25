# db.manager.py
import os
from supabase import create_client
from dotenv import load_dotenv

# load enviroment variables from .env file
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
supabase=create_client(url,key)

# user  table operations

# Create task
def create_user(name,email,password,role):
    return supabase.table("users").insert({
        "name":name,
        "email":email,
        "password":password,
        "role":role,
    }).execute()

#Get all tasks
def get_all_users():
    return supabase.table("users").select("*").execute()

#update task
def update_user(user_id, name=None, email=None, password=None, role=None):
    update_data = {}
    if name: update_data["name"] = name
    if email: update_data["email"] = email
    if password: update_data["password"] = password
    if role: update_data["role"] = role
    return supabase.table("users").update(update_data).eq("user_id", user_id).execute()


#delete task
def delete_user(user_id):
    return supabase.table("users").delete().eq("id",user_id).execute()


# Donation table operations

def create_donation(user_id, food_item, quantity, expiry_date):
    return supabase.table("donations").insert({
        "user_id": user_id,
        "food_item": food_item,
        "quantity": quantity,
        "expiry_date": expiry_date
    }).execute()
def get_all_donations():
    return supabase.table("donations").select("*").execute()
def update_donation_status(donation_id, status):
    return supabase.table("donations").update({"status": status}).eq("donation_id", donation_id).execute()
def delete_donation(donation_id):
    return supabase.table("donations").delete().eq("donation_id", donation_id).execute()

# request table operations

def create_request(ngo_id, donation_id):
    return supabase.table("requests").insert({
        "ngo_id": ngo_id,
        "donation_id": donation_id,
        "status": "pending"
    }).execute()
def get_requests_by_ngo(ngo_id):
    return supabase.table("requests").select("*").eq("ngo_id", ngo_id).execute()
def update_request_status(request_id, status):
    return supabase.table("requests").update({"status": status}).eq("request_id", request_id).execute()
def delete_request(request_id):
    return supabase.table("requests").delete().eq("request_id", request_id).execute()

