from src.db import DatabaseManager

def format_response(response, success_msg):
    """
    Convert Supabase PostgrestResponse to dict
    """
    if hasattr(response, "data") and response.data:
        return {"Success": True, "Message": success_msg, "Data": response.data}
    elif hasattr(response, "error") and response.error:
        return {"Success": False, "Message": str(response.error)}
    return {"Success": False, "Message": "Unknown error"}


class UserManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_user(self, name, email, password, role):
        if role not in ["donor", "ngo"]:
            return {"Success": False, "Message": "Invalid role"}
        response = self.db.create_user(name, email, password, role)
        return format_response(response, "User added successfully!")

    def get_users(self):
        response = self.db.get_all_users()
        return response.data if hasattr(response, "data") else []  

    def update_user(self, user_id, name=None, email=None, password=None, role=None):
        response = self.db.update_user(user_id, name, email, password, role)
        return format_response(response, "User updated successfully!")

    def delete_user(self, user_id):
        response = self.db.delete_user(user_id)
        return format_response(response, "User deleted successfully!")


class DonationManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_donation(self, user_id, food_item, quantity, expiry_date):
        response = self.db.create_donation(user_id, food_item, quantity, expiry_date)
        return format_response(response, "Donation added successfully!")

    def get_available_donations(self):
        response = self.db.get_available_donations()
        return response.data if hasattr(response, "data") else []

    def update_donation_status(self, donation_id, status):
        if status not in ["available", "accepted", "distributed"]:
            return {"Success": False, "Message": "Invalid status"}
        response = self.db.update_donation_status(donation_id, status)
        return format_response(response, "Donation status updated!")

    def delete_donation(self, donation_id):
        response = self.db.delete_donation(donation_id)
        return format_response(response, "Donation deleted successfully!")


class RequestManager:
    def __init__(self):
        self.db = DatabaseManager()

    def create_request(self, ngo_id, donation_id):
        response = self.db.create_request(ngo_id, donation_id)
        return format_response(response, "Request created successfully!")

    def get_requests_by_ngo(self, ngo_id):
        response = self.db.get_requests_by_ngo(ngo_id)
        return response.data if hasattr(response, "data") else []

    def update_request_status(self, request_id, status):
        if status not in ["pending", "accepted", "rejected"]:
            return {"Success": False, "Message": "Invalid request status"}
        response = self.db.update_request_status(request_id, status)
        return format_response(response, "Request status updated!")

    def delete_request(self, request_id):
        response = self.db.delete_request(request_id)
        return format_response(response, "Request deleted successfully!")
