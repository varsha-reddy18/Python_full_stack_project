from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# Import managers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import UserManager, DonationManager, RequestManager

# ----------------- App Setup -----------------
app = FastAPI(
    title="Food Donation and Surplus Management System API",
    version="1.0"
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Managers -----------------
user_manager = UserManager()
donation_manager = DonationManager()
request_manager = RequestManager()

# ----------------- Data Models -----------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str  # donor or ngo

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None

class DonationCreate(BaseModel):
    user_id: int
    food_item: str
    quantity: int
    expiry_date: str  # YYYY-MM-DD

class RequestModel(BaseModel):
    donation_id: int
    ngo_email: str

# ----------------- Endpoints -----------------
@app.get("/")
def home():
    return {"message": "Food donation and surplus management system API is running!"}

# ----------------- USERS -----------------
@app.get("/users")
def get_users():
    return user_manager.get_users()

@app.post("/users")
def create_user(user: UserCreate):
    result = user_manager.add_user(user.name, user.email, user.password, user.role)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    result = user_manager.update_user(user_id, user.name, user.email, user.password, user.role)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    result = user_manager.delete_user(user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ----------------- DONATIONS -----------------
@app.post("/donations")
def create_donation(donation: DonationCreate):
    result = donation_manager.add_donation(
        donation.user_id, donation.food_item, donation.quantity, donation.expiry_date
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.get("/donations")
def list_donations():
    return donation_manager.get_available_donations()

@app.put("/donations/{donation_id}/status")
def update_donation_status(donation_id: int, status: str):
    result = donation_manager.update_donation_status(donation_id, status)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/donations/{donation_id}")
def delete_donation(donation_id: int):
    result = donation_manager.delete_donation(donation_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ----------------- REQUESTS -----------------
@app.post("/requests")
def create_request(req: RequestModel):
    # Look up NGO by email
    users = user_manager.get_users()
    ngo_list = [u for u in users if u.get("email") == req.ngo_email and u.get("role") == "ngo"]

    if not ngo_list:
        raise HTTPException(status_code=404, detail="NGO not found")

    ngo_id = ngo_list[0]["user_id"]
    result = request_manager.create_request(ngo_id, req.donation_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.get("/requests/{ngo_id}")
def list_requests(ngo_id: int):
    return request_manager.get_requests_by_ngo(ngo_id)

@app.put("/requests/{request_id}/status")
def update_request_status(request_id: int, status: str):
    result = request_manager.update_request_status(request_id, status)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

@app.delete("/requests/{request_id}")
def delete_request(request_id: int):
    result = request_manager.delete_request(request_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    return result

# ----------------- Run Server -----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
